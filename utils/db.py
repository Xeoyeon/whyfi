from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class ChromaDB:
    def __init__(self, colleciton_name):
        self.embedding_model = HuggingFaceEmbeddings(
                model_name="dragonkue/BGE-m3-ko",
                multi_process=False,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},  
                # Set `True` for cosine similarity
            )
        self.vectorstore = Chroma(
    collection_name=colleciton_name, persist_directory="./chroma_db", embedding_function=self.embedding_model
    ) 
        
db = ChromaDB("words700")