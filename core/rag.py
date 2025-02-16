from .db import word_collection, book_collection
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import List
from langchain_core.documents import Document
from operator import itemgetter

load_dotenv()

class RAGAgent:
    def __init__(self, prompt_template):
        self.word_retriever = word_collection.as_retriever(search_kwargs={"k": 3})
        self.book_retriever = book_collection.as_retriever(search_kwargs={"k": 2})
        
        prompt = PromptTemplate(
            input_variables=["word_context", "book_context", "term"], 
            template=prompt_template
        )
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        
        # 병렬 검색을 위한 retriever 설정
        retriever_chain = {
            "word_context": self.word_retriever | self.format_retriever_output,
            "book_context": self.book_retriever | self.format_retriever_output,
        }
        
        self.chain = (
            {"term": RunnablePassthrough()}
            | retriever_chain
            | prompt
            | llm 
            | StrOutputParser()
        )

    def format_retriever_output(self, docs: List[Document]) -> str:
        return "\n".join([doc.page_content for doc in docs])
        
    def invoke(self, user_input: str) -> str:
        return self.chain.invoke(user_input)
        
    def stream(self, user_input: str):
        return self.chain.stream(user_input)