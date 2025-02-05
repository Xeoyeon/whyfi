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

