from core import st_agent, fetch_naver_news, fetch_google_trends, fetch_popular_keywords
import streamlit as st
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

# Streamlit 설정
st.set_page_config(page_title="WhyFi", page_icon="💰", layout="wide")

if 'term' not in st.session_state:
    st.session_state.term = ''
if 'previous_term' not in st.session_state:
    st.session_state.previous_term = ''

st.sidebar.title("📢 금융 용어 입력하기")
st.header("💰 금융 용어 알리미: WhyFi")

# 검색어 입력 필드
input_term = st.sidebar.text_input("예: 복리, 물가, ETF 등", value=st.session_state.term)

# 입력된 검색어가 변경되었을 때만 검색 실행
if input_term != st.session_state.previous_term:
    st.session_state.term = input_term
    st.session_state.previous_term = input_term

# 인기 키워드
keywords, date = fetch_popular_keywords()
st.sidebar.markdown(f'<h4 style="font-size: 16px;">📊 금융 키워드 순위 ({date})</h4>', unsafe_allow_html=True)

for i, keyword in enumerate(keywords):
    if keyword != "NEW":
        if st.sidebar.button(f"{i + 1} {keyword}"):
            st.session_state.term = keyword
            st.session_state.previous_term = keyword
            st.rerun()

st.sidebar.markdown(f'<p style="font-size: 14px;color: #555;">&copy; KDI 경제교육·정보센터 경제 키워드 트렌드</p>', unsafe_allow_html=True)

# 검색 시작
if st.session_state.term:
    st.sidebar.write("🔍 검색 중...")
    
    news_results = fetch_naver_news(st.session_state.term)
    
    with st.spinner("🔄 정보를 분석하는 중..."):
        response = st_agent.invoke(st.session_state.term)
    
    st.subheader(f"❓{st.session_state.term}")
    st.write(response)
    
    st.subheader("📰 관련 뉴스")
    if not news_results:
        st.write("❌ 관련 뉴스를 찾을 수 없습니다.")
    else:
        for news_result in news_results:
            news = f'<p><a href="{news_result["link"]}" style="color: gray;">{news_result["title"]}</a></p>'
            st.markdown(news, unsafe_allow_html=True)
    
    with st.spinner("📊 트렌드 데이터 수집 중..."):
        try:
            trends_data = fetch_google_trends(st.session_state.term)
            if not trends_data.empty:
                st.subheader(f"📈 {st.session_state.term} 검색 트렌드")
                fig = px.line(trends_data, x="Date", y="Trend Score")
                st.plotly_chart(fig)
        except Exception as e:
            print(e)
            st.warning("⚠️ 현재 트렌드 데이터를 가져올 수 없습니다. 나중에 다시 시도해 주세요.")

else:
    st.markdown("""
    <div style="font-size:14px; line-height:1.6;">
    <b>WhyFi</b>는 <b>어려운 금융이라는 주제를 쉽게 전달하고자 개발된 서비스</b>입니다.<br>
                    복잡한 금융 용어를 일상적인 언어로 설명하며, 관련된 최신 뉴스 정보를 제공합니다.<br>
    이를 통해 금융 지식에 대한 이해도를 높이고, 더 나은 금융 결정을 내릴 수 있도록 돕는 것을 목표로 합니다.
    
    ---
                    
    📌 <b>주요 기능</b>
    <ul style="list-style-type: circle; padding-left: 20px;">
        <li>사용자가 직접 입력한 금융 용어에 대한 맞춤형 답변 제공</li>
        <li>금융 용어에 대한 쉬운 설명 제공</li>
        <li>관련 뉴스와 최신 트렌드 정보 제공</li>
    </ul>
                    
    ---
    
    와이파이와 함께 금융을 쉽게 이해하고, 스마트한 금융 리터러시를 쌓아 보세요!
    </div>
    """, unsafe_allow_html=True)