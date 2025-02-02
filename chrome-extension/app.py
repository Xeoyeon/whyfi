from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
from core import agent, fetch_naver_news

app = Flask(__name__)
CORS(app)

@app.route("/explain", methods=["GET"])
def explain_term():
    term = request.args.get("term", "")
    if not term:
        return jsonify({"error": "금융 용어를 입력하세요."})

    explanation = agent.invoke(term)

    news_items = fetch_naver_news(term)
    news_list = [{"title": news["title"], "link": news["link"]} for news in news_items]

    return jsonify({"explanation": explanation, "news": news_list})

if __name__ == "__main__":
    app.run(debug=True)
