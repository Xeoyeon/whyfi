from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

class ChromaDB:
    def __init__(self, collection_name):
        self.embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
        self.vectorstore = Chroma(
            collection_name=collection_name, persist_directory="./chroma_index", embedding_function=self.embedding_model
        )

db = ChromaDB("words700")
# db = ChromaDB("stock_book")
