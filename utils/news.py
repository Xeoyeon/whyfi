import requests
import os
import random


def news_srch(query):
    try:
        client_id = os.getenv("NAVER_CLIENT_ID")
        client_secret = os.getenv("NAVER_CLIENT_SECRET")
        url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=20&sort=sim"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 오류 발생 시 예외 처리

        if response.status_code == 200:
            news_items = response.json().get("items", [])

            if not news_items:
                return "❌ 관련 뉴스를 찾을 수 없습니다."


        random_news = random.sample(news_items, min(3, len(news_items)))
        return [{"title": item['title'], "link": item['link']} for item in random_news]

    except requests.exceptions.RequestException as e:
        return f"🚨 네이버 뉴스 API 요청 실패: {e}"