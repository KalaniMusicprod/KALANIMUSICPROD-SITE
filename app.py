import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Preset Mastering Engine is Ready!"

@app.route('/master', methods=['POST'])
def master_audio():
    # 1. Check for file
    if 'target' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    target_file = request.files['target']
    
    # 2. Save file temporarily
    input_path = "temp_input.mp3"
    output_path = "mastered_output.mp3"
    target_file.save(input_path)

    try:
        # --- THE MASTERING PRESET ---
        # 1. Load the song
        sound = AudioSegment.from_file(input_path)
        
        # 2. Apply Compression (The "Glue")
        # This reduces the dynamic range so we can make it louder later without distortion.
        # Threshold: -20dB, Ratio: 4.0 (Standard mastering settings)
        compressed = compress_dynamic_range(sound, threshold=-20.0, ratio=4.0, attack=5.0, release=50.0)
        
        # 3. Apply Hard Limiting / Normalization (The "Loudness")
        # Boosts volume to -0.5dB so it doesn't clip red.
        mastered = normalize(compressed, headroom=0.5)

        # 4. Export as High-Quality MP3 (320kbps)
        # We use MP3 to keep the file size small so the server doesn't run out of RAM.
        mastered.export(output_path, format="mp3", bitrate="320k")

        # 5. Send back to user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": "Processing failed: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
