import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

@app.route("/api/webhook", methods=["POST", "GET"])
def webhook():
    # For quick browser test
    if request.method == "GET":
        return jsonify({"status": "webhook is running"}), 200

    update = request.get_json()
    print("Incoming Update:", update)

    if not update:
        return jsonify({"ok": False}), 200

    # Handle message
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Reply back
        reply = f"You said: {text}"

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return jsonify({"ok": True}), 200
