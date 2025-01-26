from dotenv import load_dotenv

import streamlit as st
from agent import agents
from utils import web_search_api

load_dotenv()

def get_response(query) :
    agent = agents['RAG']
    return agent.invoke(query)
    
def stream_response(query) :
    agent = agents['RAG']
    return agent.stream(query)
 
def invoke():
    st.title("와이파이(WhyFi) : 금융 용어 알리미")

    query = st.text_input("궁금한 금융 용어를 입력해주세요")
    result = None
    # 그래프 invoke를 실행하는 버튼
    if st.button("검색"):
        try:
            result = get_response(query=query)
        except Exception as e:
            st.error(f"An error occurred while Invoking the RAG agent: {str(e)}")
            st.stop()
    placeholder = st.empty()
    # 그래프 최종 출력이 존재할 경우에만 실행
    if result is not None:
        placeholder.markdown(result)
    # st.json(web_search_api['serper'].run(query))

def stream():
    st.title("와이파이(WhyFi) : 금융 용어 알리미")

    query = st.text_input("궁금한 금융 용어를 입력해주세요")
    # 그래프 invoke를 실행하는 버튼
    if st.button("검색"):
        try:
            st.write_stream(stream_response(query=query))
            # st.json(web_search_api['serper'].run(query))

        except Exception as e:
            st.error(f"An error occurred while Invoking the RAG agent: {str(e)}")
            st.stop()



if __name__ == "__main__":
    stream()