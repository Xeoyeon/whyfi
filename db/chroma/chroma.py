import os

import chromadb
from langchain_chroma import Chroma

from ..base import CustomDB


class CustomChroma(CustomDB):
    def __init__(self):
        super().__init__()
        self.db_path = f"{os.environ['LOCAL_DIRECTORY']}/db/chroma/chroma_db"

    def get_vector_store(self):
        if os.path.exists(self.db_path):
            persistent_client = chromadb.PersistentClient(self.db_path)
            vector_store = Chroma(
                client=persistent_client,
                collection_name="word_700",
                embedding_function=self.embedding_model,
            )
        else:
            vector_store = Chroma(
                collection_name="word_700",
                embedding_function=self.embedding_model,
                persist_directory=self.db_path,
            )
        return vector_store