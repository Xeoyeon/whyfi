from uuid import uuid4

import pandas as pd
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

"""
reference
https://huggingface.co/dragonkue/BGE-m3-ko
"""

class CustomDB:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="dragonkue/BGE-m3-ko",
            multi_process=True,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
        )
        self.db_path = None
        
    def get_vector_store(self):
        vector_store = None
        return vector_store
    
    def preprocess(self, data_path):
        df = pd.read_csv(data_path, index_col=0)
        def create_context(row):
            return Document(page_content=f"{row['Word']}: {row['Content']}", 
                            metadata={'source': '한국은행 경제금융용어 700선.pdf', 'word': row['Word']}
                            )
        df['context'] = df.apply(create_context, axis=1)
        uuids = [str(uuid4()) for _ in range(len(df['context']))]
        return df['context'].to_list(), uuids

    def load(self, data_path):
        vector_store = self.get_vector_store()
        print("loading start")
        documents, uuids = self.preprocess(data_path)
        print("preprocess complete")
        vector_store.add_documents(documents=documents, ids=uuids)