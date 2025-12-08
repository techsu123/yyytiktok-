import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set in Vercel env vars
TELEGRAM_SEND_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Import your app.py bot logic
import app  # your existing app.py functions, if any

@app.route("/api/webhook", methods=["POST", "GET"])
def webhook():
    # GET request just to test the endpoint
    if request.method == "GET":
        return jsonify({"status": "Webhook endpoint running"}), 200

    # Handle incoming Telegram updates
    update = request.get_json(force=True)
    print("Incoming Update:", update)

    # Simple example: echo text messages
    message = update.get("message")
    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        reply_text = f"You said: {text}"

        try:
            requests.post(
                TELEGRAM_SEND_URL,
                json={"chat_id": chat_id, "text": reply_text},
                timeout=10
            )
        except Exception as e:
            print("Failed to send message:", e)

    return jsonify({"ok": True})
