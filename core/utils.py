import os
import random
import requests
from pytrends.request import TrendReq
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json

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

class KeywordCrawler:
    def __init__(self):
        self.url = 'https://eiec.kdi.re.kr/bigdata/issueTrend.do'   
        self.driver = None

    def initialize_driver(self):    
        driver_path = ChromeDriverManager().install()
        correct_driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless") 

        self.driver = webdriver.Chrome(service=Service(executable_path=correct_driver_path), options=options)
        self.driver.implicitly_wait(1)
        self.driver.get(self.url)

    def get_keywords(self):
        self.initialize_driver()
        a = self.driver.find_elements(By.CLASS_NAME, 'list_updown_issue.select')  # flip_cards
        data = a[2].text #최신 키워드
        d = re.sub(r'\n\d+|\d{4}\.\d+|[-=+,#/\?:.*\"~ㆍ!‘|\(\)\[\]`\'…》\”\“\’·]', '', data)
        word= [word for word in d.split('\n') if word and word != "NEW"]
        self.driver.quit()
        return word
    
    def get_keywords_file_path(self):
        date =(datetime.now()- relativedelta(months=1)).strftime("%Y%m")
        file_path = f'./keywords/keywords_{date}.json'
        return date, file_path
    
    # 키워드 추출 및 저장 함수: 한 달에 한번씩 실행 (scheduler 활용)
    def save_keywords_to_file(self):
        keywords = self.get_keywords()
        date, file_path = self.get_keywords_file_path(date)
        data = {
            "keywords": keywords,
            "date": date
        }
        try: 
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"파일 저장 중 오류가 발생했습니다: {e}")

def fetch_popular_keywords():
    k = KeywordCrawler()
    _, file_path = k.get_keywords_file_path()
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["keywords"], data["date"]