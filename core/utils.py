import os
import random
import requests
from pytrends.request import TrendReq
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Function to fetch news from Naver API
def fetch_naver_news(query):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=50&start=2&sort=sim"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        news_items = response.json().get("items", [])
        if not news_items:
            return "관련 뉴스를 찾을 수 없습니다."
        random_news = random.sample(news_items, min(3, len(news_items)))
        return [{"title": item['title'], "link": item['link']} for item in random_news]
    
    return f"API 요청 실패: {response.status_code}"

def fetch_google_trends(term):
    pytrends = TrendReq(hl="ko", tz=540)
    pytrends.build_payload([term], timeframe='today 3-m')
    data = pytrends.interest_over_time()

    if not data.empty:
        data = data.reset_index()
        data = data.rename(columns={term:'Trend Score', 'date':'Date'})
        return data[['Date','Trend Score']]
    else:
        return pd.DataFrame(columns=['Date','Trend Score'])


def fetch_popular_keywords():
    # setup driver
    options = Options()
    options.add_argument("--headless")  # 헤드리스 모드
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)
    
    # get keywords
    url = 'https://eiec.kdi.re.kr/bigdata/issueTrend.do'   
    driver.get(url)
    data = driver.find_elements(By.CLASS_NAME, 'list_updown_issue.select')[2].text
    driver.quit()

    pattern = r'\n\d+|\d{4}\.\d+|[-=+,#/\?:.*\"~ㆍ!‘|\(\)\[\]`\'…》\”\“\’·]'
    keywords= [word for word in re.sub(pattern, '', data).split('\n') if word and word != "NEW"]
    date =(datetime.now()- relativedelta(months=1)).strftime("%Y.%m")
    return keywords, date