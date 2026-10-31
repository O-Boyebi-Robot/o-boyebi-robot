from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import requests, random, os

application = Flask(__name__)

# --- CONFIG ---
ID_PAGE = "140509102234567"  # ton ID Page O Boyebi
JETON = os.environ.get("FACEBOOK_TOKEN")  # Ton token sur Render
POSTS_VIRAUX = [
    "Mbote bandeko ! Le saviez-vous ? Kinshasa est la plus grande ville francophone au monde ! 🇨🇩",
    "Histoire : Le fleuve Congo est le 2e plus long d'Afrique après le Nil. 4.700 km de puissance !",
    "Boyebi ? Le mot 'O Boyebi' veut dire 'Tu sais ?' en Lingala. Partage si tu es fier d'être Congolais !",
    "Kinshasa La Belle ! Saviez-vous que Lola ya Bonobo est le seul sanctuaire de bonobos au monde ?",
    "Culture : La Rumba Congolaise est classée patrimoine UNESCO. On danse ? 💃🏾"
]
IMAGES = [
    "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e",
    "https://images.unsplash.com/photo-1523805009345-7448845a9e53",
    "https://images.unsplash.com/photo-1489392191049-fc10c97e64b6"
]

def auto_publish_job():
    try:
        texte = random.choice(POSTS_VIRAUX)
        image_url = random.choice(IMAGES)
        
        # Publier PHOTO + TEXTE sur ta Page
        url = f"https://graph.facebook.com/{ID_PAGE}/photos"
        data = {"url": image_url, "caption": texte, "access_token": JETON}
        r = requests.post(url, data=data)
        print(f"V6 POSTÉ: {r.json()}")
        return r.json()
    except Exception as e:
        print(f"Erreur V6: {e}")

@application.route("/")
def home():
    return {"service": "O Boyebi Robot V6 IMAGE", "status": "LIVE", "version": "V6"}

@application.route("/publish-viral")
def publier_viral():
    result = auto_publish_job()
    return {"publié": result}

# Planificateur - poste tous les jours à 08h00 heure de Kinshasa
planificateur = BackgroundScheduler(timezone="Africa/Kinshasa")
planificateur.add_job(auto_publish_job, 'cron', hour=8, minute=0)
planificateur.start()

if __name__ == "__main__":
    application.run()
