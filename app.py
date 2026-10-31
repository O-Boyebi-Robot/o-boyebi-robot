import os
import requests
from flask import Flask, request

app = Flask(__name__)

# --- CONFIG O BOYEBI ROBOT ---
PAGE_ID = "1405069442685669"
VERIFY_TOKEN = "o_boyebi_2026"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route('/', methods=['GET'])
def home():
    return "O Boyebi Robot is live 🚀", 200

@app.route('/webhook', methods=['GET'])
def verify():
    # Pour la vérification Facebook
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print(f"WEBHOOK VERIFIE pour Page {PAGE_ID}")
        return challenge, 200
    else:
        return "Erreur de verification", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"Message recu pour Page {PAGE_ID}: {data}")

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            # Verifie que c'est bien ta Page
            if str(entry.get("id")) != PAGE_ID:
                print(f"ID different ignore: {entry.get('id')}")
                continue

            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event and "text" in event["message"]:
                    text = event["message"]["text"]
                    print(f"De {sender_id}: {text}")
                    send_message(sender_id, f"Mbote ndeko ! Oyebi: {text} 😊 O Boyebi Robot ezo sala !")

    return "ok", 200

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    r = requests.post(url, json=payload)
    print(f"Envoi reponse: {r.status_code} - {r.text}")
    return r

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
