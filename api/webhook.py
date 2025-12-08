import os
from flask import Flask, request, jsonify
import requests
from config import Config
import logging

app = Flask(__name__)

# Basic logging to appear in Vercel function logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = Config.BOT_TOKEN  # set this in Vercel env vars
if not BOT_TOKEN:
    logger.warning("BOT_TOKEN is not set in environment variables.")

TELEGRAM_SEND_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/api/webhook", methods=["POST", "GET"])
def webhook():
    # Allow GET for quick manual check
    if request.method == "GET":
        return jsonify({"ok": True, "message": "Webhook endpoint. POST updates here."})

    # POST -- handle Telegram update
    try:
        update = request.get_json(force=True)
    except Exception as e:
        logger.exception("Failed to parse JSON")
        return jsonify({"ok": False, "error": "invalid json"}), 400

    logger.info("Received update: %s", update)

    # Example simple handler: echo text messages
    message = update.get("message") or {}
    chat_id = None
    text = None
    if message:
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

    if chat_id and BOT_TOKEN:
        reply_text = f"You said: {text or '<no text>'}"
        payload = {"chat_id": chat_id, "text": reply_text}
        try:
            r = requests.post(TELEGRAM_SEND_URL, json=payload, timeout=10)
            logger.info("sendMessage response: %s", r.text)
        except Exception:
            logger.exception("Failed to call sendMessage")

    # Respond 200 quickly to Telegram
    return jsonify({"ok": True})
