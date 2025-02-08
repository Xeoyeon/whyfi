import os
import streamlit as st
from utils import agent, news, pop_words
from dotenv import load_dotenv
load_dotenv()

keywords_data = pop_words.load_keywords_from_file()

if keywords_data is None:
    print("정보 업데이트 중입니다.")
    url = 'https://eiec.kdi.re.kr/bigdata/issueTrend.do'
    crawler = pop_words.KeywordCrawler(url)
    crawler.initialize_driver()
    keywords = crawler.get_keywords()
    crawler.close_driver()
    pop_words.save_keywords_to_file(keywords)  
    keywords_data = pop_words.load_keywords_from_file()


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


#사이드바
st.set_page_config(page_title="WhyFi by Euron", page_icon="💰", layout="wide")
st.sidebar.title("📌 용어를 입력하세요! ")

# 사이드바에 키워드 순위 출력
user_input = st.sidebar.text_input("예: 복리, 물가, ETF 등", value=st.session_state.user_input)
show_keywords_in_sidebar(keywords,date)

st.markdown("""
# 💰 **WhyFi** : 금융 용어 알리미
**WhyFi**는 **어려운 금융이라는 주제를 쉽게 전달하고자 개발된 서비스**입니다.
복잡한 금융 용어를 일상적인 언어로 설명하며, 관련된 최신 뉴스 정보를 제공합니다.
이를 통해 금융 지식에 대한 이해도를 높이고, 더 나은 금융 결정을 내릴 수 있도록 돕는 것을 목표로 합니다.
""")

if not user_input:
    st.markdown("""
    📌 **주요 기능** \n
    ▪️ 사용자가 직접 입력한 금융 용어에 대한 맞춤형 답변 제공 \n
    ▪️ 금융 용어에 대한 쉬운 설명 제공 \n
    ▪️ 관련 뉴스와 최신 트렌드 정보 제공 \n
    
    와이파이와 함께 금융을 쉽게 이해하고, 스마트한 금융 리터러시를 쌓아 보세요!
    """)

if user_input:
    with st.spinner("🔄 정보를 분석하는 중..."):
        news_results = news.news_srch(user_input)
        response = agent.invoke(user_input)

    st.success(f"❓{response}")  # 강조 효과

    st.subheader("📰 관련 뉴스")
    if "❌ 관련 뉴스를 찾을 수 없습니다." in news_results:
        st.warning("❌ 현재 관련된 뉴스를 찾을 수 없습니다. 다른 용어를 검색해 보세요!")
    else:
        for news in news_results:
            n = f'<p><a href="{news["link"]}" style="color: gray;">{news["title"]}</a></p>'
            st.markdown(n, unsafe_allow_html=True)

st.markdown("""
---
<footer style="text-align: right; padding: 10px; font-size: 14px; color: #555;">
    <p>&copy; Euron Research 7th WhyFi 팀. All rights reserved.</p>
    <p>ver 1.0 | Last modified 25.02.08</p>
</footer>
""", unsafe_allow_html=True)

#streamlit run c:/Users/seoyounglee/workspace/Euron/Whyfi_sy/main.py