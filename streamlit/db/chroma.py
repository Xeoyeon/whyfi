from langchain.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

class ChromaDB:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
        self.vectorstore = Chroma(
            persist_directory="./chroma_index", embedding_function=self.embedding_model
        )