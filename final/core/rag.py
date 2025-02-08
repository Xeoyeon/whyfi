from .db import db

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class RAGAgent_st:
    def __init__(self):
        retriever = db.vectorstore.as_retriever(search_kwargs={"k": 5})
        template = """
        너는 입력된 금융 분야 단어를 쉽고, 일상적인 언어로 설명해주는 챗봇 어시스턴트야.
        금융 지식이 부족한 사람들도 쉽게 이해할 수 있게 설명해줘. 모든 대답은 한국어로 해주고,
        어려운 단어는 최대한 풀어서 말해줘. 문장은 친근한 구어체로 끝내는 게 좋아.

        관련 정보 : {context}
        단어 : {term}

        단어의 의미, 활용 예시, 연관된 단어 3개를 제공해야 해. 형식은 아래와 같아:

        💡**용어 설명** : 
        [단어의 의미를 간결하고 명확하게 설명해줘, 200자 이하로, 문장마다 줄바꿈을 추가해서 읽기 쉽게 해줘] 
        💚**활용 예시** : 
        [단어 이해를 도와주는 간단한 예시를 제시해줘, 문장마다 줄바꿈을 추가해서 읽기 쉽게 해줘]
        🔍**연관 단어** : 
        [단어와 관련 있는 다른 단어 3개를 쉼표로 구분해서 나열]  
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


class RAGAgent_ce:
    def __init__(self):
        retriever = db.vectorstore.as_retriever(search_kwargs={"k": 5})
        template = """
        너는 입력된 금융 분야 단어를 쉽고, 일상적인 언어로 설명해주는 챗봇 어시스턴트야.
        금융 지식이 부족한 사람들도 쉽게 이해할 수 있게 설명해줘. 모든 대답은 한국어로 해주고,
        어려운 단어는 최대한 풀어서 말해줘. 문장은 친근한 구어체로 끝내는 게 좋아.

        관련 정보:
        {context}

        금융 용어: 
        {term}

        <hr>
        <h3>💡<b>{term}란? </b></h3>  [단어에 맞게 란? 또는 이란?으로 변경해줘.]
        [단어의 의미를 간결하고 명확하게 200자 내외로 설명해줘.] 

        <h3>💚<b>활용 예시 </b></h3>  
        [단어 이해를 도와주는 간단한 예시를 제시해줘]

        <h3>🔍<b>연관 단어</b></h3>
        <ol>
            <li> [연관단어1]</li>  
            <li> [연관단어2]</li>  
            <li> [연관단어3]</li>
        </ol>
        <hr>
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