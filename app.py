import os, requests, random
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
PAGE_ID = "1405069442685669"
VERIFY_TOKEN = "o_boyebi_2026"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
POSTS = ["LE SAVIEZ-VOUS ? Mbote bandeko ! Kinshasa est la plus grande ville francophone ! Tu le savais ?", "Bon week-end a tous les coordinateurs CNRSC MAI NDOMBE !", "O Boyebi ? Commente O Boyebi !"]
def publish(msg):
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    data = {"message": msg, "access_token": PAGE_ACCESS_TOKEN}
    return requests.post(url, data=data).json()
def auto_job():
    publish(random.choice(POSTS))
scheduler = BackgroundScheduler()
scheduler.add_job(auto_job, 'cron', hour=17, minute=0)
scheduler.start()
@app.route('/')
def home(): return "O Boyebi V4 OK", 200
@app.route('/publish-viral')
def viral():
    m = random.choice(POSTS)
    r = publish(m)
    return f"Publie: {m} - {r}", 200
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Erreur", 403
    return "ok", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
