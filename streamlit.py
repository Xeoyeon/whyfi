# SQLite3 버전 문제 해결 코드
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from core import agent, fetch_naver_news
from core.trends import get_finance_trending_keywords
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit UI
st.set_page_config(page_title="금융 용어 알리미", page_icon="💰", layout="wide")

st.sidebar.title("💰 금융 용어 알리미")
term = st.sidebar.text_input("금융 용어를 입력하세요:", "")

# ✅ 주식 인기 검색어 추가
# ✅ 실시간 금융 인기 검색어 가져오기
st.sidebar.subheader("🔥 금융 실시간 인기 검색어 TOP 3")
trending_keywords = get_finance_trending_keywords()

# ✅ 상위 3개 키워드 표시
for idx, keyword in enumerate(trending_keywords, start=1):
    st.sidebar.write(f"🏆 {idx}위: {keyword}")
    
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