import os
import random
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import requests
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

# Load Chroma VectorStore
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vectorstore = Chroma(
    persist_directory="chroma_index", embedding_function=embedding_model
)

# Define retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Load Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Function to fetch news from Naver API
def fetch_naver_news(query):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=50&start=2&sort=sim"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        news_items = response.json().get("items", [])
        if not news_items:
            return "관련 뉴스를 찾을 수 없습니다."
        random_news = random.sample(news_items, min(3, len(news_items)))
        return "\n".join([f"- {item['title']} ({item['link']})" for item in random_news])
    
    return f"API 요청 실패: {response.status_code}"

# Template
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

# Generate prompt
prompt = PromptTemplate(

    input_variables=["context", "term"], 
    template=template
)

def format_retriever_output(docs):
    return "\n".join([doc.page_content for doc in docs])

# Generate Chain
chain = (
    {
        "context": retriever,
        "term": RunnablePassthrough(),
    }
    | prompt
    | llm 
    | StrOutputParser()
)

# Streamlit UI
st.set_page_config(page_title="금융 용어 알리미", page_icon="💰", layout="wide")

st.sidebar.title("💰 금융 용어 알리미")
user_input = st.sidebar.text_input("금융 용어를 입력하세요:", "")

if user_input:
    st.sidebar.write("🔍 검색 중...")

    news_results = str(fetch_naver_news(user_input))
    retrieved_docs = retriever.invoke(user_input)
    context_text = "\n".join([doc.page_content for doc in retrieved_docs])

    with st.spinner("🔄 정보를 분석하는 중..."):
        response = chain.invoke(user_input)

    st.title("📢 금융 용어 설명")
    st.markdown(response)

    st.subheader("📰 관련 뉴스")
    if not news_results:
        st.write("❌ 관련 뉴스를 찾을 수 없습니다.")
    else:
        for news in news_results.split("\n"):
            st.markdown(news)

else:
    st.info("🔍 금융 용어를 입력하세요!")
