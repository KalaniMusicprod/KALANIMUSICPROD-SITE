import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pydub import AudioSegment, effects

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Fast Mastering Engine is Ready!"

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
        # --- FAST MASTERING (No Timeout) ---
        # 1. Load the song
        sound = AudioSegment.from_file(input_path)
        
        # 2. Normalize (The "Loudness")
        # This scans the whole song and boosts it to the max volume (-0.5dB)
        # It is very fast compared to compression.
        mastered = effects.normalize(sound, headroom=0.5)

        # 3. Export as High-Quality MP3 (320kbps)
        mastered.export(output_path, format="mp3", bitrate="320k")

        # 4. Send back to user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": "Processing failed: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
