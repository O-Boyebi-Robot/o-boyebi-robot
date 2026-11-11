import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. TES CLÉS - Elles viennent de Render > Environment
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "boyebi123")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 2. PAGE D'ACCUEIL - Pour vérifier que Render marche
@app.route("/", methods=["GET"])
def home():
    return "O Boyebi Robot est en ligne", 200

# 3. WEBHOOK - Pour Meta
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # Vérification de Meta
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Token incorrect", 403

    # Réception des messages
    if request.method == "POST":
        data = request.get_json()
        print(data)

        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for event in entry.get("messaging", []):
                    sender_id = event.get("sender", {}).get("id")
                    message = event.get("message", {})
                    texte_recu = message.get("text", "")

                    if sender_id and texte_recu:
                        reponse = generer_reponse(texte_recu)
                        envoyer_message(sender_id, reponse)
        return "OK", 200

# 4. INTELLIGENCE - O Boyebi répond
def generer_reponse(texte_recu):
    # Si tu as Gemini ou OpenAI, mets ton code ici
    # Pour l'instant, réponse simple pour tester
    prompt = f"Tu es O Boyebi, un ami de Kinshasa, drôle et motivant. L'utilisateur dit : {texte_recu}. Réponds-lui en français simple et court."
    
    # Exemple avec Gemini si tu l'as
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            result = model.generate_content(prompt)
            return result.text
        except Exception as e:
            print(f"Erreur IA: {e}")

    return f"Yo, j'ai bien reçu : {texte_recu}. Je suis O Boyebi, je suis là pour toi !"

# 5. ENVOI - Réponse sur Messenger
def envoyer_message(sender_id, texte):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": texte}
    }
    r = requests.post(url, json=payload)
    print(r.text)
    return r.json()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
