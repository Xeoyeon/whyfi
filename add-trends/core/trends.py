from pytrends.request import TrendReq
import pandas as pd

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

def fetch_google_trends_by_region(term):
    pytrends = TrendReq(hl="ko", tz=540)
    # geo="world" : 나라별 검색 트렌드 확인 가능 / TooManyRequestError 발생 
    pytrends.build_payload([term], timeframe="today 3-m", geo="KR")  
    data = pytrends.interest_by_region()

    if not data.empty:
        data = data.reset_index()
        data = data.rename(columns={term:'Trend Score', 'geoName':'Region'})
        return data[['Region','Trend Score']]
    else:
        return pd.DataFrame(columns=['Region','Trend Score'])
