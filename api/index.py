from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Telegram Bot is running</h1>"
