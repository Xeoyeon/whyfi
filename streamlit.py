__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from core import agent, fetch_naver_news
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit UI
st.set_page_config(page_title="금융 용어 알리미", page_icon="💰", layout="wide")

st.sidebar.title("💰 금융 용어 알리미")
term = st.sidebar.text_input("금융 용어를 입력하세요:", "")

if term:
    st.sidebar.write("🔍 검색 중...")

    news_results = fetch_naver_news(term)

    with st.spinner("🔄 정보를 분석하는 중..."):
        response = agent.invoke(term)

    st.title("📢 금융 용어 설명")
    st.markdown(response)

    st.subheader("📰 관련 뉴스")
    if not news_results:
        st.write("❌ 관련 뉴스를 찾을 수 없습니다.")
    else:
        for news_result in news_results:
            news = f'<p><a href="{news_result["link"]}" style="color: gray;">{news_result["title"]}</a></p>'
            st.markdown(news, unsafe_allow_html=True)

else:
    st.info("🔍 금융 용어를 입력하세요!")