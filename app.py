import os
import subprocess
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Kalani AI Mastering (Presets + Preview) is Ready!"

@app.route('/master', methods=['POST'])
def master_audio():
    if 'target' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    target_file = request.files['target']
    preset = request.form.get('preset', 'modern') # Default to Modern
    mode = request.form.get('mode', 'full')       # Default to Full Song
    
    input_path = "input_song.mp3"
    output_path = "mastered_song.mp3"
    target_file.save(input_path)

    try:
        # --- 1. DEFINE PRESETS (Ozone Styles) ---
        # Modern: Crisp highs, cut mud, loud (The "Fresh Air" vibe)
        chain_modern = "highpass=f=30,highshelf=f=10000:g=4,loudnorm=I=-12:TP=-1"
        
        # Warm: Boosts low-mids (250Hz), smooth highs, vintage vibe
        chain_warm = "highpass=f=30,lowshelf=f=250:g=2,highshelf=f=8000:g=-2,loudnorm=I=-13:TP=-1"
        
        # Bass/Trap: Boosts sub (60Hz), crispy highs (8kHz), hard limiter
        chain_bass = "highpass=f=20,lowshelf=f=60:g=4,highshelf=f=8000:g=3,loudnorm=I=-11:TP=-1"

        # Select the active chain
        if preset == 'warm':
            active_filter = chain_warm
        elif preset == 'bass':
            active_filter = chain_bass
        else:
            active_filter = chain_modern

        # --- 2. BUILD FFMPEG COMMAND ---
        command = ["ffmpeg", "-y", "-i", input_path]

        # Check for Preview Mode (Only process first 30 seconds)
        if mode == 'preview':
            command.extend(["-t", "30"]) 

        # Add filters and quality settings
        command.extend([
            "-af", active_filter,
            "-b:a", "320k",
            output_path
        ])
        
        # Run FFmpeg
        subprocess.run(command, check=True)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": "Processing failed: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
