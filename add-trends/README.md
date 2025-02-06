### 수정사항
- 구글 pytrends 패키지를 활용하여 검색 트렌드 분석 추가
    - streamlit : 검색 트렌드 그래프 추가 
    - chrome extension : 간단한 분석만 추가 (최고, 최저, 평균 스코어)
- RAG template 수정
  - 서영님 template 참고해서 구어체로, 가독성있게 출력하도록 변경 
- streamlit과 chrome extension의 RAGAgent 분리
  - chrome extension template에 html tag 추가하기 위함
- streamlit & chrome extension UI 변경
  - 서영님 markdown 참고해서 서비스 설명 추가
  - 기타 문구 변경

(추가) pytrends 429 error : try-except 처리하여 오류 뜨더라도 나머지 결과는 출력되도록 수정
    
---

### streamlit 화면 
| ![Image 1](https://github.com/user-attachments/assets/c1950169-f3e6-4967-93a7-b72d7dfd090c) | ![Image 2](https://github.com/user-attachments/assets/b70e802d-d02e-4a86-8224-81d866aa84c0) |
|:---:|:---:|
| 검색어 입력 전 화면| 검색어("환율") 입력 후 화면|

---

### chrome extension 화면
| ![image](https://github.com/user-attachments/assets/080ddb9f-43e2-4a6e-a8ad-3f07176a6205) | ![image](https://github.com/user-attachments/assets/c85415d4-89d9-4e53-9706-0cb9e17b2e51) | ![image](https://github.com/user-attachments/assets/d7073904-20a2-4bfd-899b-1ece7d43bded)|
| :---: | :---: | :---: |
| 검색어 입력 전 화면 | 검색어("환율") 입력 후 화면 1 | 검색어("환율") 입력 후 화면 2 |



