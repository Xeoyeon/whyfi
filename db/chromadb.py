from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import chromadb
import pandas as pd
from uuid import uuid4
import os

class CustomChroma:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="dragonkue/BGE-m3-ko",
            multi_process=True,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
        )
        self.vector_store = self.get_vector_store()
        
    def get_vector_store(self):
        if os.path.isdir("directory_path"):
            persistent_client = chromadb.PersistentClient()
            vector_store = Chroma(
                client=persistent_client,
                collection_name="word_700",
                embedding_function=self.embedding_model,
            )
        else:
            vector_store = Chroma(
                collection_name="word_700",
                embedding_function=self.embedding_model,
                persist_directory="./chroma_db",  # Where to save data locally, remove if not necessary
            )
        return vector_store

    def load(self, data_path):
        print("loading start")
        df = pd.read_csv(data_path)
        def create_context(row):
            return Document(page_content=f"{row['Word']}: {row['Content']}", 
                            metadata={'source': '한국은행 경제금융용어 700선.pdf', 'word': row['Word']}
                            )
        df['context'] = df.apply(create_context, axis=1)
        uuids = [str(uuid4()) for _ in range(len(df['context']))]

        self.vector_store.add_documents(documents=df['context'].to_list(), ids=uuids)