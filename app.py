# O-BOYEBI ROBOT - Version V13 PRO
# Code Language: ENGLISH
# Robot Language: French + Lingala
# Functions: Publish 3x/day + Auto Reply to Comments
# Brain: Google Gemini FREE

import os
import logging
import requests
import random
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# ================= CONFIG =================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("O-Boyebi-Robot")

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "boyebi123")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
FB_BASE = "https://graph.facebook.com/v21.0"

# ================= THEMES =================
THEMES = [
    "motivation to succeed in Congo, never give up",
    "business and mbongo: how to start small in Kinshasa",
    "bolingo and couple: big brother advice",
    "discipline and hard work makasi",
    "faith and hope for young people in Kin",
    "Congolese pride, RDC makasi",
    "advice for beginner entrepreneurs in Kinshasa"
]

# ================= 1. GEMINI BRAIN =================
def call_gemini(prompt):
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 500}
    }
    try:
        r = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", headers={"Content-Type": "application/json"}, json=data, timeout=35)
        res = r.json()
        text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
        return text
    except Exception as e:
        logger.error(f"❌ Gemini error: {e}")
        return None

def generate_post_text():
    theme = random.choice(THEMES)
    # Prompt tells AI to write in French + Lingala, even if code is in English
    prompt = f"""You are O Boyebi, the most viral creator in Congo.
Write a VIRAL Facebook post in FRENCH + LINGALA about: {theme}.

STRICT RULES:
- Mix simple Kinshasa French + Lingala words (ex: eloko, makasi, bolingo, ndeko, mbongo, kitoko, tozo kende)
- Start with a SHOCK HOOK with 🔥 or 💪 or ❤️
- 3 to 5 short
