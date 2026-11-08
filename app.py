import os
import logging
import requests
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import random

# CONFIG
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("o-boyebi")

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
PAGE_ID = os.getenv("PAGE_ID", "")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "o-boyebi-123")
FB_BASE = "https://graph.facebook.com/v21.0"
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

THEMES = [
    "Motivation pour reussir au Congo",
    "Conseils pour entreprendre a Kinshasa",
    "Discipline et travail acharne",
    "Foi et espoir pour les jeunes de Kin",
    "Fierte congolaise, RDC",
    "Conseils aux entrepreneurs debutants a Kinshasa",
    "Histoire inspirante de Kinshasa"
]

# CERVEAU GEMINI
def call_gemini(prompt):
    if not GEMINI_API_KEY:
        return "Salut, c'est O Boyebi ! Comment je peux t'aider aujourd'hui ?"
    try:
        url = f"{URL_GEMINI}?key={GEMINI_API_KEY}"
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7}
        }
        res = requests.post(url, json=data, timeout=30)
        result = res.json()
        texte = result["candidates"][0]["content"]["parts"][0]["text"]
        return texte.strip()
    except Exception as e:
        logger.error(f"Erreur Gemini: {e}")
        return "Salut, c'est O Boyebi ! Je suis la pour toi, pose-moi ta question."

def generer_texte_post():
    theme = random.choice(THEMES)
    prompt = (
        "Tu es O Boyebi, le createur le plus viral du Congo. "
        f"Theme du jour: {theme}. "
        "Ecris une publication Facebook virale en francais simple de Kinshasa melange avec un peu de Lingala. "
        "REGLES STRICTES: "
        "1. Commence avec un HOOK tres fort qui arrete le scroll. "
        "2. Texte
