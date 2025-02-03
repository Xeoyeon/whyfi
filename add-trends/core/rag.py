from .db import db

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class RAGAgent:
    def __init__(self):
        retriever = db.vectorstore.as_retriever(search_kwargs={"k": 5})
        template = """
        당신은 금융 전문가입니다.
        사용자가 입력한 금융 용어를 누구나 이해하기 쉽고 간단하게 설명합니다. 필요하면 이해를 돕기 위한 예시도 설명에 포함합니다.
        그리고 그 용어와 연관된 검색어 3개를 제공합니다. 

        관련 정보:
        {context}

        금융 용어:
        {term}

        💡{term}란?: 

        🔍연관 검색어:
        """
        prompt = PromptTemplate(input_variables=["context", "term"], template=template)

        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        self.chain = (
            {
                "context": retriever | self.format_retriever_output,
                "term": RunnablePassthrough(),
            }
            | prompt
            | llm 
            | StrOutputParser()
        )
    def format_retriever_output(self, docs):
        return "\n".join([doc.page_content for doc in docs])
        
    def invoke(self, user_input):
        return self.chain.invoke(user_input)
    
    def stream(self, user_input):
        return self.chain.stream(user_input)
