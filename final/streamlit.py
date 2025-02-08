# pip install pytrends
# pip install plotly

from core import agent_st, fetch_naver_news
import streamlit as st
from dotenv import load_dotenv
import plotly.express as px 
import matplotlib.pyplot as plt
import re

load_dotenv()

# Streamlit UI
st.set_page_config(page_title="WhyFi", page_icon="💰", layout="wide")

st.sidebar.title("📢 금융 용어 입력하기")
term = st.sidebar.text_input("예: 복리, 주식, ETF 등등", "")

st.header("💰 금융 용어 알리미: WhyFi")

if not term:
    st.markdown("""
    <div style="font-size:14px; line-height:1.6;">
    <b>WhyFi</b>는 <b>어려운 금융이라는 주제를 쉽게 전달하고자 개발된 서비스</b>입니다.<br>                
    복잡한 금융 용어를 일상적인 언어로 설명하며, 관련된 최신 뉴스 정보를 제공합니다.<br>
    이를 통해 금융 지식에 대한 이해도를 높이고, 더 나은 금융 결정을 내릴 수 있도록 돕는 것을 목표로 합니다.  
    <br><br>
                          
    📌 <b>주요 기능</b>  
    <ul style="list-style-type: circle; padding-left: 20px;">
        <li>사용자가 직접 입력한 금융 용어에 대한 맞춤형 답변 제공</li>
        <li>금융 용어에 대한 쉬운 설명 제공</li>
        <li>관련 뉴스와 최신 트렌드 정보 제공</li>
    </ul>
    
    와이파이와 함께 금융을 쉽게 이해하고, 스마트한 금융 리터러시를 쌓아 보세요!
    </div>
    """, unsafe_allow_html=True)


if term:
    status = st.sidebar.empty()
    status.write("🔍 검색 중...")

    news_results = fetch_naver_news(term)

    with st.spinner("🔄 정보를 분석하는 중..."):
        response = agent_st.invoke(term)

    st.subheader(f"❓{term}")
    st.success(f"{response}")

    st.markdown("---")
    st.subheader("📰 관련 뉴스")
    if not news_results:
        st.write("❌ 관련 뉴스를 찾을 수 없습니다.")
    else:
        for news_result in news_results:
            news = f'<p><a href="{news_result["link"]}" style="color: gray;">{news_result["title"]}</a></p>'
            st.markdown(news, unsafe_allow_html=True)
    
    status.empty()
    st.sidebar.write("⭐ 검색 완료 !")

else:
    st.sidebar.info("🔍 금융 용어를 입력하세요!")

st.markdown("""
---
<footer style="text-align: right; padding: 10px; font-size: 14px; color: #555;">
    <p>&copy; Euron Research 7th WhyFi 팀. All rights reserved.</p>
    <p>ver 1.0 | Last modified 25.02.08</p>
</footer>
""", unsafe_allow_html=True)