from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
import google.generativeai as genai
import requests
import streamlit as st
import random

from dotenv import load_dotenv
load_dotenv()
os.chdir('C:\\Users\\seoyounglee\\workspace\\Euron\\Whyfi')

from pop_words import KeywordCrawler, save_keywords_to_file, load_keywords_from_file
keywords_data = load_keywords_from_file()

if keywords_data is None:
    print("데이터가 없으므로 크롬 드라이버를 초기화하고 크롤링을 시작합니다.")
    url = 'https://eiec.kdi.re.kr/bigdata/issueTrend.do'
    crawler = KeywordCrawler(url)
    crawler.initialize_driver()
    keywords = crawler.get_keywords()
    crawler.close_driver()
    save_keywords_to_file(keywords)  
    keywords_data = load_keywords_from_file()


keywords = keywords_data["keywords"]
date = keywords_data["date"]

if 'user_input' not in st.session_state: st.session_state.user_input = '' 

def show_keywords_in_sidebar(data,date):
    st.sidebar.markdown(f'<h4 style="font-size: 16px;">📊 금융 키워드 순위 ({date})</h4>', unsafe_allow_html=True)    
    number_to_unicode = {
    1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤", 6: "⑥", 7: "⑦", 8: "⑧", 9: "⑨", 10: "⑩"
    }
    for i, keyword in enumerate(data):
        if keyword != "NEW":
            #st.sidebar.write(f"{i + 1}. {keyword}")
            if st.sidebar.button(f"{number_to_unicode.get(i + 1, i + 1)} {keyword}"):
                # 버튼 클릭 시 user_input에 해당 키워드를 저장
                st.session_state.user_input = keyword  # 세션 상태에 키워드를 저장
                st.rerun()
    
    st.sidebar.markdown(f'<p style="font-size: 14px;color: #555;">&copy; KDI 경제교육·정보센터 경제 키워드 트렌드</p>', unsafe_allow_html=True)


embedding_model = HuggingFaceEmbeddings(
                model_name="dragonkue/BGE-m3-ko",
                multi_process=False,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},  
                # Set `True` for cosine similarity
            )

vector_store = Chroma(
    persist_directory="chroma_db", embedding_function=embedding_model
    ) 

#retriever = emb.as_retriever(search_kwargs={"k": 5})
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)

def news_srch(query):
    try:
        client_id = os.getenv("NAVER_CLIENT_ID")
        client_secret = os.getenv("NAVER_CLIENT_SECRET")
        url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=20&sort=sim"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 오류 발생 시 예외 처리

        if response.status_code == 200:
            news_items = response.json().get("items", [])

            if not news_items:
                return "❌ 관련 뉴스를 찾을 수 없습니다."


        random_news = random.sample(news_items, min(5, len(news_items)))
        return "\n".join([f"- [{item['title']}]({item['link']})" for item in random_news])

    except requests.exceptions.RequestException as e:
        return f"🚨 네이버 뉴스 API 요청 실패: {e}"

template = '''
너는 입력된 금융 분야 단어를 쉽고, 일상적인 언어로 설명해주는 챗봇 어시스턴트야.
금융 지식이 부족한 사람들도 쉽게 이해할 수 있게 설명해줘. 모든 대답은 한국어로 해주고,
어려운 단어는 최대한 풀어서 말해줘. 문장은 친근한 구어체로 끝내는 게 좋아.

단어의 의미, 활용 예시, 연관된 단어 3개를 제공해야 해. 형식은 아래와 같아:

검색어 : [단어]  

정의 : [단어의 의미를 간결하고 명확하게 설명해줘, 200자 이하로, 설명 끝마다 줄바꿈을 추가해서 읽기 쉽게 해줘] 
활용 예시 : [단어를 자연스럽게 포함한 문장 예시]  
연관 단어 : [단어와 관련 있는 다른 단어 3개를 쉼표로 구분해서 나열]  

Question: {question}
'''

prompt = PromptTemplate(
    input_variables=["question"], 
    template=template
)

def format_retriever_output(docs):
    return "\n".join([doc.page_content for doc in docs])

chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm 
    | StrOutputParser()
)



#사이드바
st.set_page_config(page_title="WhyFi by Euron", page_icon="💰", layout="wide")
st.sidebar.title("📌 궁금한 금융 용어를 입력하세요! ")

# 사이드바에 키워드 순위 출력
user_input = st.sidebar.text_input("예: 복리, 주식, ETF 등", value=st.session_state.user_input)
show_keywords_in_sidebar(keywords,date)

st.markdown("""
# 💰 **WhyFi** : 금융 용어 알리미
**WhyFi**는 **어려운 금융이라는 주제를 쉽게 전달하고자 개발된 서비스**입니다.
복잡한 금융 용어를 일상적인 언어로 설명하며, 관련된 최신 뉴스 정보를 제공합니다.
이를 통해 금융 지식에 대한 이해도를 높이고, 더 나은 금융 결정을 내릴 수 있도록 돕는 것을 목표로 합니다.

📌 **주요 기능** \n
▪️ 사용자가 직접 입력한 금융 용어에 대한 맞춤형 답변 제공 \n
▪️ 금융 용어에 대한 쉬운 설명 제공 \n
▪️ 관련 뉴스와 최신 트렌드 정보 제공 \n

와이파이와 함께 금융을 쉽게 이해하고, 스마트한 금융 리터러시를 쌓아 보세요!
""")

if user_input:
    with st.spinner("🔄 정보를 분석하는 중..."):
        news_results = news_srch(user_input)
        retrieved_docs = retriever.invoke(user_input)
        response = chain.invoke(user_input)

    st.success(f"❓{response}")  # 강조 효과

    st.subheader("📰 관련 뉴스")
    if "❌ 관련 뉴스를 찾을 수 없습니다." in news_results:
        st.warning("❌ 현재 관련된 뉴스를 찾을 수 없습니다. 다른 용어를 검색해 보세요!")
    else:
        for news in news_results.split("\n"):
            #st.markdown(f"[{item['title']}]({item['link']})")
            st.markdown(news, unsafe_allow_html=True)

st.markdown("""
---
<footer style="text-align: right; padding: 10px; font-size: 14px; color: #555;">
    <p>&copy; Euron Research 7th WhyFi 팀. All rights reserved.</p>
    <p>ver 1.0 | Last modified 25.02.02</p>
</footer>
""", unsafe_allow_html=True)

#streamlit run c:/Users/seoyounglee/workspace/Euron/Whyfi/main.py
#git clone https://github.com/4rldur0/whyfi.git
# cd whyfi
# streamlit run streamlit.py
# python app.py