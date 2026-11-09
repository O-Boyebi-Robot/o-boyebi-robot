import os
import logging
import requests
import random
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("o-boyebi")
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
PAGE_ID = os.getenv("PAGE_ID", "")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "o-boyebi-123")
FB_BASE = "https://graph.facebook.com/v21.0
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
THEMES = [
    "Motivation pour reussir au Congo",
    "Conseils pour entreprendre a Kinshasa",
    "Discipline et travail",
    "Foi et espoir pour les jeunes",
    "Fierte congolaise RDC",
    "Conseils pour les entrepreneurs debutants",
    "Histoire inspirante de Kinshasa"
]

def call_gemini(prompt):
    if not GEMINI_API_KEY:
def call_gemini(prompt):
    if not GEMINI_API_KEY:
        return "Salut, c'est O Boyebi ! Comment je peux t'aider ?"
    try:
        url = URL_GEMINI + "?key=" + GEMINI_API_KEY
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        res = requests.post(url, json=data, timeout=30)
        logger.error(f"GEMINI STATUS: {res.status_code} - {res.text[:500]}")
        if res.status_code != 200:
            return "Salut, c'est O Boyebi ! Je suis la pour toi."
        result = res.json()
        texte = result["candidates"][0]["content"]["parts"][0]["text"]
        return texte.strip()
    except Exception as e:
        logger.error(f"Erreur Gemini: {e}")
        return "Salut, c'est O Boyebi ! Je suis la pour toi."
def generer_texte_post():
    theme = random.choice(THEMES)
    prompt = "Tu es O Boyebi, le createur le plus viral du Congo. Theme: " + theme + ". Ecris une publication Facebook virale en francais simple de Kinshasa avec un peu de Lingala. Commence avec un HOOK tres fort. Texte court, 3 a 5 phrases max. Ajoute 3 hashtags a la fin. Ton motivant et drole."
    return call_gemini(prompt)

def envoyer_message_facebook(recipient_id, texte):
    if not PAGE_ACCESS_TOKEN:
        return
    url = FB_BASE + "/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    data = {"recipient": {"id": recipient_id}, "message": {"text": texte[:1900]}}
    try:
        requests.post(url, params=params, json=data, timeout=20)
    except Exception as e:
        logger.error("Erreur envoi FB")

def publier_sur_page(texte):
    if not PAGE_ACCESS_TOKEN or not PAGE_ID:
        return
    url = FB_BASE + "/" + PAGE_ID + "/feed"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    data = {"message": texte}
    try:
        requests.post(url, params=params, data=data, timeout=20)
    except Exception as e:
        logger.error("Erreur publication")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "O Boyebi Robot est en ligne"})

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Token invalide", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for event in entry.get("messaging", []):
                    sender_id = event["sender"]["id"]
                    if "message" in event and "text" in event["message"]:
                        texte_recu = event["message"]["text"]
                        prompt_reponse = "Tu es O Boyebi, un ami de Kinshasa, drole et motivant, qui parle francais simple avec du Lingala. Un fan te dit: " + texte_recu + ". Reponds en 2-3 phrases courtes et chaleureuses."
                        reponse = call_gemini(prompt_reponse)
                        envoyer_message_facebook(sender_id, reponse)
        return "OK", 200
    except Exception as e:
        logger.error("Erreur webhook")
        return "OK", 200

@app.route("/test-post", methods=["GET"])
def test_post():
    texte = generer_texte_post()
    return jsonify({"post_genere": texte})

def tache_quotidienne():
    logger.info("Generation du post quotidien")
    texte = generer_texte_post()
    publier_sur_page(texte)

scheduler = BackgroundScheduler()
scheduler.add_job(tache_quotidienne, "cron", hour=8, minute=0)
scheduler.start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
