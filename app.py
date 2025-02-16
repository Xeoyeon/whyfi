from core import ce_agent, fetch_naver_news, fetch_google_trends, fetch_popular_keywords
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/explain", methods=["GET"])
def explain_term():
    term = request.args.get("term", "")
    if not term:
        return jsonify({"error": "금융 용어를 입력하세요."})
    
    explanation = ce_agent.invoke(term)
    news_items = fetch_naver_news(term)
    trend_summary = ""  # 기본값 설정
    
    try:
        trend = fetch_google_trends(term)
        if not trend.empty:
            avg_trend = round(trend['Trend Score'].mean(), 2)
            peak_trend = trend.loc[trend['Trend Score'].idxmax()]
            lowest_trend = trend.loc[trend['Trend Score'].idxmin()]
            
            # 문자열로 가공
            trend_summary = f"평균 관심도: {avg_trend}\n"
            trend_summary += f"최고 관심도: {int(peak_trend['Trend Score'])} ({peak_trend['Date'].strftime('%Y-%m-%d')})\n"
            trend_summary += f"최저 관심도: {int(lowest_trend['Trend Score'])} ({lowest_trend['Date'].strftime('%Y-%m-%d')})"
            
    except Exception as e:
        print(f"Google Trends 데이터 가져오기 오류: {e}")
        trend_summary = ""  # 에러 시 빈 문자열 설정
    
    return jsonify({
        "explanation": explanation,
        "news": news_items,
        "trend": trend_summary,
    })

@app.route("/keywords", methods=["GET"])  # POST에서 GET으로 변경
def get_keywords():
    keywords, date = fetch_popular_keywords()
    return jsonify({
        "keywords": keywords,
        "date": date,
    })

if __name__ == "__main__":
    app.run(debug=True)