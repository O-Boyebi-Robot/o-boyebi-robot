import os, requests, random
from flask import Flask, request
app = Flask(__name__)
PAGE_ID = "1405069442685669"
VERIFY_TOKEN = "o_boyebi_2026"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
POSTS = ["Mbote bandeko! O Boyebi ?", "Bon week-end CNRSC MAI NDOMBE!", "Kinshasa ville francophone!"]
def publish(m):
 url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
 return requests.post(url, data={"message": m, "access_token": PAGE_ACCESS_TOKEN}).json()
@app.route('/')
def home(): return "OK V4", 200
@app.route('/publish-viral')
def viral():
 r = publish(random.choice(POSTS))
 return f"OK {r}", 200
@app.route('/webhook', methods=['GET','POST'])
def webhook():
 if request.method == 'GET':
  if request.args.get("hub.verify_token") == VERIFY_TOKEN:
   return request.args.get("hub.challenge"), 200
  return "Erreur", 403
 return "ok", 200
if __name__ == "__main__":
 app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
