from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """
    <html><body>
      <h2>yyytiktok — Telegram webhook ready</h2>
      <p>Use <code>/api/webhook</code> to receive Telegram updates.</p>
    </body></html>
    """, 200, {"Content-Type": "text/html"}
