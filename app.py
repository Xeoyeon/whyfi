from core import agent, fetch_naver_news

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/explain", methods=["GET"])
def explain_term():
    term = request.args.get("term", "")
    if not term:
        return jsonify({"error": "금융 용어를 입력하세요."})

    explanation = agent.invoke(term)

    news_items = fetch_naver_news(term)
    return jsonify({"explanation": explanation, "news": news_items})

if __name__ == "__main__":
    app.run(debug=True)
