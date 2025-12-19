import os
import matchering as mg
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Kalani Mastering Engine is Ready!"

@app.route('/master', methods=['POST'])
def master_audio():
    # Check if user sent both files
    if 'target' not in request.files or 'reference' not in request.files:
        return jsonify({"error": "Missing files! Please upload both Target and Reference."}), 400
    
    target_file = request.files['target']
    reference_file = request.files['reference']
    
    # Save files temporarily
    target_path = "temp_target.wav"
    reference_path = "temp_reference.wav"
    output_path = "mastered_output.wav"
    
    target_file.save(target_path)
    reference_file.save(reference_path)

    try:
        # --- THE MASTERING PROCESS ---
        # This copies the mastering of the reference onto the target
        mg.process(
            target=target_path,
            reference=reference_path,
            results=[mg.pcm16(output_path)]
        )

        # Send the file back to the user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": "Processing failed: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
