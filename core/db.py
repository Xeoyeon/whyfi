from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

class ChromaDB:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    def get_collection(self, colleciton_name: str):
        return Chroma(
            collection_name=colleciton_name, persist_directory="./chroma_index", embedding_function=self.embedding_model
        )

db = ChromaDB()

word_collection = db.get_collection("words700")
book_collection = db.get_collection("stock_book")