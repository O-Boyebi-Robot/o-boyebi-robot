from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import requests, random, os

application = Flask(__name__)

# --- CONFIG CORRIGEE ---
ID_PAGE = "1405099442685669"  # Ton vrai ID O Boyebi Robot
JETON = os.environ.get("META_PAGE_ACCESS_TOKEN") or os.environ.get("FACEBOOK_TOKEN")

POSTS_VIRAUX = [
    "Mbote bandeko ! Le saviez-vous ? Kinshasa est la plus grande ville francophone au monde ! 🇨🇩",
    "Histoire : Le fleuve Congo est le 2e plus long d'Afrique apres le Nil. 4.700 km de puissance !",
    "Boyebi ? Le mot 'O Boyebi' veut dire 'Tu sais ?' en Lingala. Partage si tu es fier d'etre Congolais !",
    "Kinshasa La Belle ! Saviez-vous que Lola ya Bonobo est le seul sanctuaire de bonobos au monde ?",
    "Culture : La Rumba Congolaise est classee patrimoine UNESCO. On danse ?"
]

IMAGES = [
    "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e",
    "https://images.unsplash.com/photo-1523805009345-7448845a9e53",
    "https://images.unsplash.com/photo-1489392191049-fc10c97e64b6"
]

def auto_publish_job():
    if not JETON:
        print("ERREUR: Token manquant")
        return {"erreur": "Token manquant"}
    try:
        texte = random.choice(POSTS_VIRAUX)
        image_url = random.choice(IMAGES)
        url = f"https://graph.facebook.com/v19.0/{ID_PAGE}/photos"
        data = {"url": image_url, "caption": texte, "access_token": JETON}
        r = requests.post(url, data=data, timeout=30)
        print(f"V6 POSTE: {r.status_code} {r.json()}")
        return r.json()
    except Exception as e:
        print(f"Erreur V6: {e}")
        return {"erreur": str(e)}

@application.route("/")
def home():
    return {"service": "O Boyebi Robot V6 IMAGE", "status": "LIVE", "version": "V6.2", "page_id": ID_PAGE, "token_ok": bool(JETON)}

@application.route("/publish-viral")
def publier_viral():
    result = auto_publish_job()
    return {"publie": result}

planificateur = BackgroundScheduler(timezone="Africa/Kinshasa")
planificateur.add_job(auto_publish_job, 'cron', hour=8, minute=0)
planificateur.start()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
