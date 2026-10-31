import os, requests, random
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
PAGE_ID = "1405069442685669"
VERIFY_TOKEN = "o_boyebi_2026"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VIRAL_POSTS = ["🤔 LE SAVIEZ-VOUS ? Mbote bandeko ! Kinshasa est la 3e plus grande ville d'Afrique ! Tu le savais ? 👇","Bon week-end à tous les coordinateurs CNRSC MAI NDOMBE ! 🙏","🔥 O Boyebi ? Commente O Boyebi si tu vois ce post !"]
def publish_to_page(message):
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    data = {"message": message, "access_token": PAGE_ACCESS_TOKEN}
    return requests.post(url, data=data).json()
def publish_auto_daily():
    publish_to_page(random.choice(VIRAL_POSTS))
scheduler = BackgroundScheduler()
scheduler.add_job(publish_auto_daily, 'cron', hour=17, minute=0)
scheduler.start()
@app.route('/')
def home(): return "O Boyebi V4 Live", 200
@app.route('/publish-viral')
def publish_viral():
    msg = random.choice(VIRAL_POSTS)
    result = publish_to_page(msg)
    return f"Publié: {msg} {result}", 200
@app.route('/publish')
def publish_custom():
    text = request.args.get("text", "Mbote !")
    result = publish_to_page(text)
    return f"Publié: {text} {result}", 200
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token")==VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Erreur", 403
    return "ok", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
