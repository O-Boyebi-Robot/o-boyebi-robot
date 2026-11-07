import os
import logging
import requests
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("O-Boyebi-Robot")

app = Flask(__name__)

# Tes clés - elles sont dans Render, jamais dans le code
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "boyebi123")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"
FB_URL = f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"

# --- 1. LE CERVEAU GRATUIT : GROQ ---
def generate_text():
    """Génère un post viral en français avec Groq (gratuit)"""
    prompt = """Tu es O Boyebi, un créateur de contenu viral au Congo.
Écris un post Facebook court, puissant, en français simple avec un peu de lingala.
Sujet : motivation, business, amour, ou actualité positive.
Structure : 1 phrase choc + 2-3 phrases de valeur + 1 question pour les commentaires + 3 hashtags.
Ton : chaleureux, direct, comme un grand frère de Kinshasa.
Maximum 120 mots. Pas de guillemets au début."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
        "max_tokens": 400
    }

    try:
        r = requests.post(GROQ_URL, headers=headers, json=data, timeout=30)
        result = r.json()
        text = result["choices"][0]["message"]["content"].strip()
        logger.info(f"Texte généré: {text[:80]}...")
        return text
    except Exception as e:
        logger.error(f"Groq error: {e}")
        # Texte de secours si Groq est down
        return "🔥 O Boyebi ! Ne lâche jamais. Le succès commence par un petit pas aujourd'hui. Tu es capable de plus que tu ne penses. Tu en penses quoi ? #OBoyebi #Motivation #Kinshasa"

# --- 2. LA BOUCHE : PUBLIER SUR FACEBOOK ---
def publish_post():
    """Génère et publie automatiquement"""
    if not PAGE_ACCESS_TOKEN or not PAGE_ID:
        logger.error("PAGE_ID ou PAGE_ACCESS_TOKEN manquant dans Render")
        return {"error": "config manquante"}

    text = generate_text()
    payload = {
        "message": text,
        "access_token": PAGE_ACCESS_TOKEN
    }
    try:
        r = requests.post(FB_URL, data=payload, timeout=30)
        result = r.json()
        logger.info(f"Publish result: {r.status_code} {result}")
        return result
    except Exception as e:
        logger.error(f"Publish error: {e}")
        return {"error": str(e)}

# --- 3. ROUTES ---
@app.route("/")
def home():
    return jsonify({
        "service": "O Boyebi Robot",
        "status": "LIVE",
        "version": "V8.0 Professional - Groq Gratuit",
        "page_id": PAGE_ID,
        "groq_configured": bool(GROQ_API_KEY),
        "token_configured": bool(PAGE_ACCESS_TOKEN)
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": str(datetime.now())})

@app.route("/publish-viral")
def publish_viral():
    result = publish_post()
    return jsonify({"published": result})

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # Vérification Facebook
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Token invalide", 403
    # Réception des messages
    data = request.get_json()
    logger.info(f"Webhook reçu: {data}")
    return "OK", 200

# --- 4. SCHEDULER : Publie tous les jours à 08:00 Kinshasa ---
scheduler = BackgroundScheduler(timezone="Africa/Kinshasa")
scheduler.add_job(publish_post, 'cron', hour=8, minute=0)
scheduler.add_job(publish_post, 'cron', hour=12, minute=0)
scheduler.add_job(publish_post, 'cron', hour=18, minute=0)
scheduler.start()
logger.info("Scheduler started - 3 posts/jour: 08h, 12h, 18h Kinshasa")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
