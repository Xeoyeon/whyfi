from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load Chroma VectorStore
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vectorstore = Chroma(persist_directory="chroma_index", embedding_function=embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# 네이버 뉴스 검색
def fetch_naver_news(query):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=3&sort=sim"
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("items", [])
    return []

# Template
template = """
당신은 금융 전문가입니다.
사용자가 입력한 금융 용어를 누구나 이해하기 쉽고 간단하게 설명합니다. 필요하면 이해를 돕기 위한 예시도 설명에 포함합니다.
그리고 그 용어와 연관된 검색어 3개를 제공합니다. 

관련 정보:
{context}

금융 용어: 
{term}

👉설명: 

🕶️연관 검색어: 
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

@app.route("/explain", methods=["GET"])
def explain_term():
    term = request.args.get("term", "")
    if not term:
        return jsonify({"error": "금융 용어를 입력하세요."})

    retrieved_docs = retriever.invoke(term)
    context_text = "\n".join([doc.page_content for doc in retrieved_docs])
    explanation = chain.invoke(term)

    # 네이버 뉴스 검색
    news_items = fetch_naver_news(term)
    news_list = [{"title": news["title"], "link": news["link"]} for news in news_items]

    return jsonify({"explanation": explanation, "news": news_list})

if __name__ == "__main__":
    app.run(debug=True)