# tavily
## output example
```
[
    {'url': 'https://onepickk.tistory.com/17', 
    'content': '경상수지란 무엇인지, 흑자와 적자의 차이, 그로 인한 경제적 영향까지 자세히 알아보세요. 경상수지의 개념과 중요성, 최신 사례를 통해 경제를 이해하는 데 필요한 모든 정보를 제공합니다 경상수지란 한 나라가 외국과의 경제적 거래에서 발생하는 모든 거래를 포함한 국제수지 항목의 하나'}, 
    {'url': 'https://enertravel.tistory.com/entry/무역통계-용어-정리-경상수지-무역수지-뜻-차이점', 
    'content': '경상수지의 의미: 경상수지는 상기 4가지를 합산한 수지로 종합적인 경제체력을 진단하는 지표로 쓰입니다. 경상수지가 흑자일 경우, 한 나라가 해외로부터 벌어들이는 돈이 더 많다는 것을 의미합니다. 반면, 적자일 경우 해외에 지출한 돈이 더 많다는 뜻입니다.'}, 
    {'url': 'https://sin7375.tistory.com/entry/경상수지란-무엇인가경제학-올바르게-이해하기', 
    'content': '경상수지가 흑자일 경우, 이는 외환 보유고가 증가하고, 국가의 신용도가 높아지는 긍정적인 효과를 가져옵니다. 반면, 경상수지가 적자일 경우, 이는 외환 보유고가 감소하고, 국가의 신용도가 낮아지는 부정적인 영향을 미칠 수 있습니다.'}
]
```
## 사용
- 1000 credits/month
- "~에 관한 뉴스"와 같이 쿼리 변환 필요


# serper
## output example
```
{'searchParameters': 
    {'q': '경상수지가 뭐야?', 'gl': 'kr', 'hl': 'ko', 'type': 'news', 'num': 10, 'engine': 'google'}, 
'news': 
    [
        {'title': '경상수지 5개월 연속 흑자, 내년 트럼프 2기에선 몇백억 달러 손실?', 
        'link': 'https://newneek.co/@headlight/article/14037', 
        'snippet': "우리나라 경상수지*가 5개월 연속 흑자를 기록했어요. 경상수지는 간단히 말해 '외국과 발생한 다양한 거래에서 우리가 얼마나 돈을 벌었는지'를...", 
        'date': '2024. 11. 8.', 
        'source': '뉴닉', 
        'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR50yESLrtFeUDArXg-wzeaou969kYuxcGNKgx9eZ5-oSGmef-DlNILPKA&usqp=CAI&s', 
        'position': 1},
        {'title': '1월 경상수지 30억5천만 달러 흑자…9개월 연속 파란불', 
        'link': 'https://www.khan.co.kr/article/202403081049011', 
        'snippet': '지난 1월 우리나라 경상수지가 30억5000만 달러 흑자를 기록했다. 9개월 연속 흑자다. 반도체를 중심으로 수출이 증가한 영향이다.', 'date': '2024. 3. 8.', 'source': '경향신문', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVy_e_7uKXRStrtAsMn7siUMdnGTeknV_uEaRGyObSd86vFd_0JoyUhxk&usqp=CAI&s', 'position': 2}, {'title': '수출 살아났다, 경상수지 10개월 연속 흑자', 'link': 'https://www.chosun.com/economy/economy_general/2024/04/06/SUBD4W5MGVGGRIVHHTWEQGYFYM/', 'snippet': '지난 2월 경상수지가 68억6000만달러 흑자를 기록했다고 한국은행이 5일 밝혔다. 흑자 폭은 1월(30억5000만달러)에 비해 2배 이상으로 커졌다.', 'date': '2024. 4. 6.', 'source': '조선일보', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQwiOICKs3_wd9FyeaNCJbBfaf-yCYXXhiSxZFPvayJPK2fWUUvaoPiK8&usqp=CAI&s', 'position': 3}, {'title': '‘경상수지 1년 만에 적자’, 무슨 얘기야?', 'link': 'https://newneek.co/@headlight/article/9332', 'snippet': "'경제잘알' 되고 싶은데 경제뉴스 보면 '저게 무슨 소리야' 했나요? 지금 뜨는 헤드라인 경제뉴스, 헤드라이트가 가뿐하게 풀어드려요.", 'date': '2024. 6. 12.', 'source': '뉴닉', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8P_elteYhTEYDDi0FA15qUHaGEPGhsmy-5ICpp4CFn83by-u5wOcztkY&usqp=CAI&s', 'position': 4}, {'title': '경상수지란?', 'link': 'https://www.hani.co.kr/arti/economy/finance/461384.html', 'snippet': '경상수지는 소득을 이루는 요소들이 국가 간에 오고 간 결과의 차이를 보여주는 것입니다. 즉 생산 활동의 결과물입니다. 자본수지는 소득을 이루지 않는...', 'date': '2019. 10. 20.', 'source': '한겨레', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ81Re99WAzLDcsSzVA4RXWK4qoXt6bDPJG8RYKqu0SO6i0ReUGaoY6V-A&usqp=CAI&s', 'position': 5}, {'title': '사상 최대 경상수지 적자!', 'link': 'https://brunch.co.kr/@sbaconnect/9', 'snippet': '우리나라 이대로 괜찮을까...? | 관련 개념 설명 경상수지: 국가 간에 이루어지는 상품 및 서비스 거래인 경상거래에 의한 결과를 종합한 것으로,...', 'date': '2023. 5. 29.', 'source': '브런치스토리', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFZLU85nVL5jDVqiMygtRc8eAVmYVoe9CvTdHTDAc&usqp=CAI&s', 'position': 6}, {'title': '[한방에 정리! 알쏭달쏭 경제용어] 경상수지 2개월 연속 적자 … 지속땐 원화값 하락', 'link': 'https://www.mk.co.kr/news/society/10714557', 'snippet': '지난 2월 우리나라 경상수지가 두 달 연속 적자를 기록했다. 경상수지가 2개월 연속 적자를 낸 것은 유가가 크게 오르고 남유럽 재정 위기의 영향을...', 'date': '2023. 4. 17.', 'source': '매일경제', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWmZsohagbwILE1eoCp8LGFdZtB0pBbQ208lxAAMtu2oJx89A5ettcyfM&usqp=CAI&s', 'position': 7}, {'title': '[집중분석]작년 나라별 경상수지 ′희비교차′...＂中서 손해, 美서 만회＂', 'link': 'https://sateconomy.co.kr/news/view/1065605902136810', 'snippet': '한은 ′2022년 지역별 국제수지′ 발표, 21년만에 대중 경상 적자 미국 사상 최대 흑자 기록...EU 흑자전환, 일본은 적자폭 줄어대 중국 수출감소 폭...', 'date': '2023. 6. 22.', 'source': '토요경제', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS22Y6PrJU9IoJ8rSpUqPh7E8n12hvOEdh20WzIBO1s7hLgd9toDkVXnkE&usqp=CAI&s', 'position': 8}, {'title': '韓 6월 경상수지 58.7억 달러 흑자..."불황형 아냐"', 'link': 'https://zdnet.co.kr/view/?no=20230808102401', 'snippet': '국내 6월 경상수지가 58억7천만 달러(약 7조6천750억원) 흑자를 기록했다. 수출이 증가한 것 보다 수입이 줄어든 것을 두고 내수부진에 따른 불황형...', 'date': '2023. 8. 8.', 'source': '지디넷코리아', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmLlTkUxozQ4wARTFLQbAz5uBCe2hZrXVvxvi34CEKO-bEpil_lR0gnu8&usqp=CAI&s', 'position': 9}, {'title': '5월 경상수지 흑자 전환…상품흑자는 5년4개월만에 최저(종합)', 'link': 'https://www.yna.co.kr/view/AKR20190704019451002', 'snippet': '(서울=연합뉴스) 이지헌 정수연 기자 = 지난 4월 7년 만에 적자를 기록했던 경상수지가 5월 들어 흑자를 회복했다.', 'date': '2019. 7. 4.', 'source': '연합뉴스', 'imageUrl': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSelOQABldIQq_vELPwXhi0EWoruahqkERJdQxWSDVvRsn2nQN30kiZTc&usqp=CAI&s', 'position': 10}], 'credits': 1}
```
## 사용
- 2500 credits
- 예시 코드
    ```
    results = web_search_tools['serper'].run(query)['news']
    for result in results:
        st.markdown(f"[{result['title']}]({result['link']})")
    ```

# 비교
- serper가 쿼리 변환 없이 뉴스만 가져올 수 있으므로 사용하기 더 편함
- 다만 한 달 사용랑이 1000인 tavily와 달리 총 credit이 2500임