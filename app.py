from flask import Flask, request
import os, requests
from openai import OpenAI
app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "o_boyebi_2026")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "O Boyebi Robot en ligne!"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Erreur", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
