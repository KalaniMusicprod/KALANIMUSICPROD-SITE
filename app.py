import os
import subprocess
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Pro AI Mastering Engine (Crispy & Loud) is Ready!"

@app.route('/master', methods=['POST'])
def master_audio():
    # 1. Check for file
    if 'target' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    target_file = request.files['target']
    
    # 2. Save file temporarily
    input_path = "input_song.mp3"
    output_path = "mastered_song.mp3"
    target_file.save(input_path)

    try:
        # --- THE "CRISPY & LOUD" CHAIN ---
        # 1. highpass=f=30: Removes deep mud (Clarity)
        # 2. highshelf=f=10000:g=4: Boosts highs by 4dB (The "Fresh Air" Crispiness)
        # 3. loudnorm=I=-12:TP=-1: Smart Limiter targeting -12 LUFS volume
        
        filter_chain = "highpass=f=30,highshelf=f=10000:g=4,loudnorm=I=-12:TP=-1"

        command = [
            "ffmpeg", 
            "-y",  # Overwrite output
            "-i", input_path,
            "-af", filter_chain, 
            "-b:a", "320k", # High Quality 320kbps
            output_path
        ]
        
        # Run the command
        subprocess.run(command, check=True)

        # 3. Send back to user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": "Processing failed: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
