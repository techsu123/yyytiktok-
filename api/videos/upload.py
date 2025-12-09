from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/videos/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400
    
    video = request.files['video']
    description = request.form.get('description', '')
    
    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video.save(filepath)
        
        # Process video (thumbnail generation, compression, etc.)
        return jsonify({
            'message': 'Video uploaded successfully',
            'filename': filename,
            'description': description,
            'url': f'/uploads/{filename}'
        })
    
    return jsonify({'error': 'File type not allowed'}), 400
