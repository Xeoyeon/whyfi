from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import re
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 파일 저장할 경로 지정
def get_keywords_file_path():
    base_dir = 'C:\\Users\\seoyounglee\\workspace\\Euron\\Whyfi_sy'
    keywords_dir = os.path.join(base_dir, 'keyword')
    date = (datetime.now() - relativedelta(months=1)).strftime("%Y.%m")
    return os.path.join(keywords_dir, f"keywords_{date}.json")

# 키워드 추출 및 저장 함수
def save_keywords_to_file(keywords):
    file_path = get_keywords_file_path()
    date =(datetime.now()- relativedelta(months=1)).strftime("%Y.%m")
    
    data = {
        "keywords": keywords,
        "date": date
    }
    try: 
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

# 키워드 불러오기 함수
def load_keywords_from_file():
    file_path = get_keywords_file_path()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


class KeywordCrawler:
    def __init__(self, url):
        self.url = url
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
        a = self.driver.find_elements(By.CLASS_NAME, 'list_updown_issue.select')  # flip_cards
        data = a[2].text #최신 키워드
        d = re.sub(r'\n\d+|\d{4}\.\d+|[-=+,#/\?:.*\"~ㆍ!‘|\(\)\[\]`\'…》\”\“\’·]', '', data)
        word= [word for word in d.split('\n') if word and word != "NEW"]
        return word

    def close_driver(self):
        if self.driver:
            self.driver.quit()
