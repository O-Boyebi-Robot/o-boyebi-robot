
import os
import requests
import random
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

PAGE_ID = "1405069442685669"
VERIFY_TOKEN = "o_boyebi_2026"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

POSTS_VIRAUX = [
    "🤔 OYEBI ? Le saviez-vous ? Kinshasa a plus de 17 millions d'habitants ! Commente OYEBI si tu es Kinois 👇 #OBoyebi #RDC",
    "Mbote ba ndeko ! 🇨🇩 MOT DU JOUR : 'Boyebi = Connaissance'. Partage si tu es fier d'être Congolais ! ❤️",
    "🎁 JEU : Commente 'O BOYEBI' + tag 2 amis ! Tirage à 20h ce soir ! Bonne chance 🍀 #Kinshasa",
    "💡 ASTUCE FACEBOOK : Pour avoir beaucoup de likes, publie à 18h et pose une question à la fin ! Tu veux plus d'astuces ? Dis 'ASTUCE' en inbox",
    "🔥 VRAI OU FAUX ? La RDC a 26 provinces. Réponds en commentaire ! Le premier qui trouve a un cadeau !",
    "Mbote famille O Boyebi ! ❤️ Si tu vois ce post, laisse un ❤️ et je m'abonne à toi en retour ! On grandit ensemble !",
    "🎵 OYEBI NINI ? Quelle est ta chanson Congolaise préférée du moment ? Commente !",
    "🚀 Objectif 10K abonnés ! On est déjà 1405... Merci ! Invite 3 amis aujourd'hui et on y arrive ! #OBoyebiRobot"
]

def publish_to_page(message):
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed?access_token={PAGE_ACCESS_TOKEN}"
    r = requests.post(url, json={"message": message})
    print(f"[AUTO-PUBLISH 18h] {r.status_code} - {r.text} - Message: {message}")
    return r

def publish_auto_daily():
    msg = random.choice(POSTS_VIRAUX)
    print(f"Publication auto 18h Kinshasa : {msg}")
    publish_to_page(msg)

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {"recipient": {"id": recipient_id}, "message": {"text": message_text}}
    requests.post(url, json=payload)

# --- SCHEDULER 18h Kinshasa = 17h UTC ---
scheduler = BackgroundScheduler()
scheduler.add_job(publish_auto_daily, 'cron', hour=17, minute=0) # 18h Kinshasa
scheduler.start()
print("Scheduler démarré - Publication auto à 18h Kinshasa")

@app.route('/', methods=['GET'])
def home():
    return "O Boyebi Robot LIVE + Auto 18h Kin", 200

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Erreur", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event and "text" in event["message"]:
                    txt = event["message"]["text"]
                    txt_low = txt.lower()
                    if "publie" in txt_low:
                        m = txt.replace("publie","").strip()
                        publish_to_page(m if len(m)>3 else random.choice(POSTS_VIRAUX))
                        send_message(sender_id, "Publié ✅")
                    else:
                        send_message(sender_id, f"Mbote ! {txt} 😊 Tape ABONNE pour soutenir la page !")
    return "ok", 200

@app.route('/publish-viral', methods=['GET'])
def publish_viral():
    text = random.choice(POSTS_VIRAUX)
    publish_to_page(text)
    return f"Publié maintenant : {text}", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
