import os
import random

import requests

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