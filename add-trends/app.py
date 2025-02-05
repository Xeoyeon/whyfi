from core import agent_ce, fetch_naver_news, fetch_google_trends
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
    explanation = agent_ce.invoke(term)
    news_items = fetch_naver_news(term)
    
    trend = fetch_google_trends(term)
    if trend.empty:
        trend_summary = {
            "average_score": "",
            "peak_date": "",
            "peak_score": "",
            "lowest_date": "",
            "lowest_score": ""
        }
    else:
        avg_trend = round(trend['Trend Score'].mean(), 2)
        peak_trend = trend.loc[trend['Trend Score'].idxmax()]
        lowest_trend = trend.loc[trend['Trend Score'].idxmin()]
        trend_summary = {
            "average_score": avg_trend,
            "peak_date": peak_trend['Date'].strftime('%Y-%m-%d'),
            "peak_score": int(peak_trend['Trend Score']),
            "lowest_date": lowest_trend['Date'].strftime('%Y-%m-%d'),
            "lowest_score": int(lowest_trend['Trend Score'])
        }
    
    return jsonify({
        "explanation": explanation, 
        "news": news_items,
        "trend": trend_summary
    })

if __name__ == "__main__":
    app.run(debug=True)
