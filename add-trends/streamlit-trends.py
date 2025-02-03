# pip install pytrends
# pip install plotly

from core import agent, fetch_naver_news, fetch_google_trends
import streamlit as st
from dotenv import load_dotenv
import plotly.express as px 
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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
    st.write(response)

    st.subheader("📰 관련 뉴스")
    if not news_results:
        st.write("❌ 관련 뉴스를 찾을 수 없습니다.")
    else:
        for news_result in news_results:
            news = f'<p><a href="{news_result["link"]}" style="color: gray;">{news_result["title"]}</a></p>'
            st.markdown(news, unsafe_allow_html=True)
    
    st.subheader(f"📈 {term} 검색 트렌드")
    with st.spinner("📊 트렌드 데이터 수집 중..."):
        trends_data = fetch_google_trends(term)
    if not trends_data.empty:
        fig = px.line(trends_data, x="Date", y="Trend Score")
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ 트렌드 데이터를 찾을 수 없습니다.")
else:
    st.info("🔍 금융 용어를 입력하세요!")