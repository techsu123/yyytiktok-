import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # configured in Vercel env vars

TELEGRAM_SEND_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/api/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") != "application/json":
        return jsonify({"ok": False, "reason": "invalid content-type"}), 400

    update = request.get_json(force=True)

    # Basic safety check
    if not update:
        return jsonify({"ok": False, "reason": "no body"}), 400

    # Example: when a user sends a message, echo it back
    message = update.get("message")
    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        reply_text = f"You said: {text}"

        payload = {"chat_id": chat_id, "text": reply_text}
        # send message back to user
        resp = requests.post(TELEGRAM_SEND_URL, json=payload, timeout=10)

    # Always respond 200 to Telegram quickly
    return jsonify({"ok": True})

