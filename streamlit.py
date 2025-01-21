from agent import RAGAgent
import streamlit as st

def whyfi_search_word(question) :
    template = """
    <|system|>
    You are a helpful assistant.<|end|>
    <|user|>
    {question}<|end|>
    <|assistant|>
    """
    agent = RAGAgent(prompt_template=template)
    result = agent.invoke(question)
    return result
    
def main():
    st.title("와이파이(WhyFi) : 금융 용어 알리미")

    question = st.text_input("궁금한 금융 용어를 입력해주세요")
    result = None
    # 그래프 invoke를 실행하는 버튼
    if st.button("Search"):
        try:
            result = whyfi_search_word(question=question)
        except Exception as e:
            st.error(f"An error occurred while Invoking the RAG agent: {str(e)}")
            st.stop()
    placeholder = st.empty()
    # 그래프 최종 출력이 존재할 경우에만 실행
    if result is not None:
        placeholder.markdown(result)

if __name__ == "__main__":
    main()