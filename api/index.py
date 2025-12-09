from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# TikTok API routes
@app.route('/')
def home():
    return jsonify({
        "message": "TikTok API is running",
        "status": "success",
        "endpoints": [
            "/api/videos",
            "/api/users",
            "/api/auth"
        ]
    })

@app.route('/api/videos', methods=['GET'])
def get_videos():
    # Sample video data
    videos = [
        {
            "id": 1,
            "url": "https://example.com/video1.mp4",
            "title": "Trending Dance",
            "likes": 1000,
            "comments": 50,
            "shares": 200
        },
        {
            "id": 2,
            "url": "https://example.com/video2.mp4",
            "title": "Funny Cats",
            "likes": 5000,
            "comments": 300,
            "shares": 1000
        }
    ]
    return jsonify({"videos": videos})

@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file"}), 400
    
    video_file = request.files['video']
    # Process video upload here
    return jsonify({"message": "Video uploaded successfully"})

if __name__ == '__main__':
    app.run(debug=True)
