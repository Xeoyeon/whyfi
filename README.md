# WhyFi
Euron 7기 와이파이(WhyFi) : 금융 용어 알리미 팀의 레포지토리입니다.

### 프로젝트 소개
LangChain 기반 RAG Agent 구현 (BGE-m3-ko + Gemini 1.5)
- LangChain을 활용하여 RAG 파이프라인 구성
- ChromaDB를 벡터스토어로 사용하여 금융 용어 검색
- LangChain의 PyPDFLoader로 파싱 및 BGE-m3-ko 임베딩 모델을 이용하여 벡터 변환 및 유사도 검색
- Gemini 1.5를 기반으로 자연스러운 한국어 응답 생성
- streamlit을 활용한 유저 친화적인 UI 구현 및 로컬 배포 & 크롬 확장 프로그램으로도 제공

### 25.01.26 업데이트
- ChromaDB에 "경제금융용어 700선(한국은행)" 자료 구축 완료
- 네이버 뉴스 API를 활용하여 검색 단어 관련 뉴스 리턴하는 기능 추가

### 25.02.02 업데이트
- ChromaDB에 "2024 한권으로 OK 주식과 세금(국세청)" 자료 추가 구축 완료
- 뉴스가 중복되는 문제를 막기 위해 관련 뉴스들 중 3개를 랜덤 추출하는 아이디어 적용 완료
- streamlit UI 보완 완료

### 25.02.08 업데이트
- KDI 경제교육·정보센터에서 제공하는 지난달 Top 10 경제 키워드를 크롤링하여 순위 보여주는 기능 추가
- 키워드 버튼을 클릭하면 해당 키워드로 바로 검색이 가능하도록 수정 완료

|검색 전|검색 후|
|---|---|
|![image](https://github.com/user-attachments/assets/b0efe678-6c2f-4b07-8a91-d041a931f3ea) | ![image](https://github.com/user-attachments/assets/2788517c-4fe1-4324-a85b-a04502421747) |
