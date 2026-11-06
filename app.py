from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import random
import os
import logging

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Configuration ---
PAGE_ID = "1405099442685669"
PAGE_ACCESS_TOKEN = os.environ.get("META_PAGE_ACCESS_TOKEN") or os.environ.get("FACEBOOK_TOKEN") or os.environ.get("PAGE_ACCESS_TOKEN")
GRAPH_API_VERSION = "v19.0"

VIRAL_POSTS = [
    "Mbote bandeko! Did you know? Kinshasa is the largest French-speaking city in the world! 🇨🇩",
    "History: The Congo River is the 2nd longest river in Africa after the Nile. 4,700 km of power!",
    "Boyebi? The word 'O Boyebi' means 'Do you know?' in Lingala. Share if you are proud to be Congolese!",
    "Kinshasa La Belle! Did you know Lola ya Bonobo is the only bonobo sanctuary in the world?",
    "Culture: Congolese Rumba is UNESCO heritage. Let's dance?"
]

IMAGES = [
    "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e",
    "https://images.unsplash.com/photo-1523805009345-7448845a9e53",
    "https://images.unsplash.com/photo-1489392191049-fc10c97e64b6"
]

def publish_post():
    """Publish a random viral post with image to Facebook Page."""
    if not PAGE_ACCESS_TOKEN:
        logger.error("Missing PAGE_ACCESS_TOKEN")
        return {"error": "Missing PAGE_ACCESS_TOKEN"}

    text = random.choice(VIRAL_POSTS)
    image_url = random.choice(IMAGES)
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PAGE_ID}/photos"

    payload = {
        "url": image_url,
        "caption": text,
        "access_token": PAGE_ACCESS_TOKEN
    }

    try:
        response = requests.post(url, data=payload, timeout=30)
        result = response.json()
        logger.info(f"Publish result: {response.status_code} {result}")
        return result
    except Exception as e:
        logger.error(f"Publish error: {e}")
        return {"error": str(e)}

@app.route("/")
def home():
    return jsonify({
        "service": "O Boyebi Robot",
        "status": "LIVE",
        "version": "V7.0 Professional",
        "page_id": PAGE_ID,
        "token_configured": bool(PAGE_ACCESS_TOKEN)
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/publish-viral")
def publish_viral():
    result = publish_post()
    return jsonify({"published": result})

# --- Scheduler: Every day at 08:00 Kinshasa time ---
scheduler = BackgroundScheduler(timezone="Africa/Kinshasa")
scheduler.add_job(publish_post, 'cron', hour=8, minute=0)
scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
