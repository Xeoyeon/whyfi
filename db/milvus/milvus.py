import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from pymilvus import DataType, MilvusClient
import os

from utils import BGEM3EmbeddingFunction
from ..base import CustomDB

"""
reference
https://python.langchain.com/docs/integrations/retrievers/milvus_hybrid_search/ : hybrid search
https://milvus.io/docs/install_standalone-docker.md : 나중에 도커 환경에서 돌릴 때 참고하기
"""

class CustomMilvus(CustomDB):
    def __init__(self):
        super().__init__()
        self.sparse_model_name: str = "upskyy/e5-small-korean"
        self.dense_model_name: str = "upskyy/bge-m3-korean"

        print("load sparse model...")
        self.sparse_emb_fn = HuggingFaceEmbeddings(
            model_name=self.sparse_model_name,
            model_kwargs={'device':'cpu'},
        )

        self.dim_sparse = 384  # e5-small dimension
        self.dim_dense = 1024  # BGE-M3 dimension

        self.db_path = f"{os.environ['LOCAL_DIRECTORY']}/db/milvus/milvus_db.db"

    def get_vector_store(self):
        vector_store = Milvus(
            embedding_function=self.embedding_model,
            connection_args={"uri": self.db_path},
        )
        return vector_store

# ========================== without langchain_milvus ============================

    def preprocess_v2(self, data_path):
        print("load dense model...")
        # dense_embedding_function = HuggingFaceEmbeddings(
        #     model_name=self.dense_model_name,
        # )
        dense_emb_fn = BGEM3EmbeddingFunction()
        df = pd.read_csv(data_path, index_col=0)
        print("preprocessing...")
        df['text'] = df.apply(lambda x: f"{x['Word']}: {x['Content']}", axis=1)
        df.rename(columns={'Word': 'word'}, inplace=True)
        df.drop(columns=['Content'], inplace = True)
        df['source'] = ['한국은행 경제금융용어 700선.pdf'] * len(df)
        df['sparse_vector'] = self.sparse_emb_fn.embed_documents(df['text'])
        print("sparse vector generated")
        df['dense_vector'] = dense_emb_fn.embed_df(df=df, col='text')
        print("dense vector generated")
        return df.to_dict('records')

    def get_milvus_client(self):
        client = MilvusClient(self.db_path)
        return client

    def get_index_params(self, client):
        index_params = client.prepare_index_params()
        index_params.add_index(
            field_name="dense_vector",
            index_type="IVF_FLAT",
            metric_type="COSINE",
            params={"M": 48, "efConstruction": 200},
        )
        index_params.add_index(
            field_name="sparse_vector",
            index_type="IVF_FLAT",
            metric_type="COSINE",
            params={"nlist": 1024},
        )
        return index_params

    def get_schema(self, client):
        schema = client.create_schema(
            auto_id=True,
            enable_dynamic_fields=False,
        )
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True, max_length=100)
        schema.add_field(field_name="sparse_vector", datatype=DataType.FLOAT_VECTOR, dim=self.dim_sparse)
        schema.add_field(field_name="dense_vector", datatype=DataType.FLOAT_VECTOR, dim=self.dim_dense)
        schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=10000)
        schema.add_field(field_name="word", datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name="source", datatype=DataType.VARCHAR, max_length=1000)
        return schema
    
    def create_collection(self, client, collection_name):
        index_params = self.get_index_params(client)
        schema = self.get_schema(client)
        client.create_collection(
            collection_name=collection_name,
            schema=schema,
            auto_id=True,
            vector_field_name="vector",
            enable_dynamic_field=False,
            index_params=index_params,
            consistency_level="Strong"
        )

    def insert(self, data_path, collection_name):
        data = self.preprocess_v2(data_path)
        print("inserting...")
        client = self.get_milvus_client()
        if not client.has_collection(collection_name=collection_name):
            self.create_collection(client=client, collection_name=collection_name)
        client.insert(collection_name=collection_name, data=data)