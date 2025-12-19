import os
import subprocess
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Urban AI Mastering Engine (Trap/Drill/Afro) is Ready!"

@app.route('/master', methods=['POST'])
def master_audio():
    if 'target' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    target_file = request.files['target']
    preset = request.form.get('preset', 'fresh') 
    mode = request.form.get('mode', 'full')       
    
    input_path = "input_song.mp3"
    output_path = "mastered_song.mp3"
    target_file.save(input_path)

    try:
        # --- SCIENTIFIC URBAN MASTERING CHAINS ---

        # 1. TRAP & DRILL (Heavy 808s, Sharp Highs)
        # - Highpass 20Hz: Cleans ultra-low rumble
        # - Lowshelf 60Hz (+4dB): Boosts the 808 sub-bass specifically
        # - Cut 300Hz (-2dB): Removes "boxiness" to clean up mud
        # - Highshelf 8kHz (+3dB): Makes hi-hats sharp
        # - Loudnorm -9 LUFS: Competitive volume for Trap
        chain_trap = "highpass=f=20,lowshelf=f=60:g=4,equalizer=f=300:t=q:w=1:g=-2,highshelf=f=8000:g=3,loudnorm=I=-9:TP=-0.5"
        
        # 2. REGGAETON & AFROBEAT (Punchy Kick, Clear Vocals)
        # - Highpass 30Hz: Tightens the kick drum
        # - Lowshelf 100Hz (+2dB): Adds weight to the Reggaeton Kick
        # - Boost 2kHz (+2dB): "Vocal Presence" boost so voice cuts through beat
        # - Highshelf 12kHz (+2dB): Smooth Air (not harsh)
        # - Loudnorm -10 LUFS: Loud but keeps the bounce/dynamics
        chain_afro = "highpass=f=30,lowshelf=f=100:g=2,equalizer=f=2000:t=q:w=1:g=2,highshelf=f=12000:g=2,loudnorm=I=-10:TP=-1"

        # 3. FRESH & CRISPY (The "Fresh Air" VST Sound)
        # - Highpass 40Hz: Very clean low end
        # - Highshelf 10kHz (+5dB): The "Fresh Air" effect (Massive clarity)
        # - Highshelf 16kHz (+3dB): Extra "Sparkle"
        # - Loudnorm -11 LUFS: Balanced commercial loudness
        chain_fresh = "highpass=f=40,highshelf=f=10000:g=5,highshelf=f=16000:g=3,loudnorm=I=-11:TP=-1"

        # Select Chain
        if preset == 'trap':
            active_filter = chain_trap
        elif preset == 'afro':
            active_filter = chain_afro
        else:
            active_filter = chain_fresh

        # Build Command
        command = ["ffmpeg", "-y", "-i", input_path]

        if mode == 'preview':
            command.extend(["-t", "30"]) 

        command.extend([
            "-af", active_filter,
            "-b:a", "320k",
            output_path
        ])
        
        subprocess.run(command, check=True)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": "Processing failed: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
