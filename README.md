# whyfi
Euron 7기 와이파이(WhyFi) : 금융 용어 알리미 팀의 레포지토리입니다.

HuggingFace spaces에서 해당 앱을 실행해 볼 수 있습니다 👉 [WhyFi:금융용어알리미](https://huggingface.co/spaces/xeoyeon/whyfi)

### 프로젝트 소개
LangChain 기반 RAG Agent 구현 (BGE-m3-ko + Gemini 1.5)
- LangChain을 활용하여 RAG 파이프라인 구성
- ChromaDB를 벡터스토어로 사용하여 금융 용어 검색
- LangChain의 PyPDFLoader로 파싱 및 BGE-m3-ko 임베딩 모델을 이용하여 벡터 변환 및 유사도 검색
- Gemini 1.5를 기반으로 자연스러운 한국어 응답 생성
- streamlit을 활용한 유저 친화적인 UI 구현 및 로컬 배포 & 크롬 확장 프로그램으로도 제공


### streamlit 실행
1. 
    ```(bash)
    $ streamlit run streamlit.py
    ```
2. 
    http://localhost:8501 접속

### chrome extension 실행
1. 
    ```(bash)
    $ python3 app.py
    ```
2. 
    chrome://extensions/에서 개발자 모드로 변경 후 `chrome-extension` 폴더 로드
