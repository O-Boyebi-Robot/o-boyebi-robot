import os, random, logging, requests
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
PAGE_ID = "1405069442685669"
VERIFY_TOKEN = "o_boyebi_2026"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
POSTS_VIRAUX = [
 "LE SAVIEZ-VOUS ? Mbote bandeko ! Kinshasa est la plus grande ville francophone du monde !",
 "O Boyebi ? Commente O Boyebi si tu es fier d'etre Congolais !",
 "Debat du jour : Pondu, Fumbwa ou Madesu ?",
 "Mot du jour : Eloko veut dire Chose en Lingala.",
 "Histoire : Le fleuve Congo est le 2e plus puissant au monde !",
 "Question : Citez 3 provinces de la RDC ! Go !",
 "Bon debut de semaine a tous les Congolais !"
]
def publish_to_facebook(message):
    if not PAGE_ACCESS_TOKEN: return {"error": "Token manquant"}
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    return requests.post(url, data={"message": message, "access_token": PAGE_ACCESS_TOKEN}).json()
def auto_publish_job():
    publish_to_facebook(random.choice(POSTS_VIRAUX))
scheduler = BackgroundScheduler(timezone="Africa/Kinshasa")
scheduler.add_job(auto_publish_job, 'cron', hour=18, minute=0)
scheduler.start()
@app.route('/')
def home(): return jsonify({"status": "LIVE", "service": "O Boyebi Robot V5 PRO"}), 200
@app.route('/publish-viral')
def publish_viral():
    msg = random.choice(POSTS_VIRAUX)
    return jsonify({"published": msg, "facebook_result": publish_to_facebook(msg)}), 200
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Token invalide", 403
    return "ok", 200
