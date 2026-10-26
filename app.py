from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "o_boyebi_2026")

@app.route("/")
def home():
    return "O Boyebi Robot en ligne!"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Erreur", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    return "ok", 200
