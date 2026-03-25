from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime, timedelta
import sqlite3
from crypto_utils import generate_key_from_audio, encrypt_data

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to connect to DB
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. Check karo ki file aur audio dono aaye hain ya nahi
    if 'file' not in request.files or 'audio' not in request.files:
        return jsonify({"error": "Missing file or audio key"}), 400

    file = request.files['file']
    audio = request.files['audio']
    plan = request.form.get('plan', 'free') # Default free plan

    # 2. Temporary audio save karo key nikalne ke liye
    temp_audio_path = "temp_key.wav"
    audio.save(temp_audio_path)
    
    try:
        # 3. Audio se Key generate karo
        key = generate_key_from_audio(temp_audio_path)
        
        # 4. Original file read karo aur encrypt karo
        file_data = file.read()
        encrypted_content = encrypt_data(file_data, key)

        # 5. Unique Room Code aur encrypted filename banao
        room_code = str(uuid.uuid4())[:8].upper() # Example: A1B2C3D4
        encrypted_filename = f"{room_code}.enc"
        file_path = os.path.join(UPLOAD_FOLDER, encrypted_filename)

        # 6. Encrypted file save karo
        with open(file_path, 'wb') as f:
            f.write(encrypted_content)

        # 7. Database mein entry karo
        expiry = datetime.now() + (timedelta(days=1) if plan == 'free' else timedelta(days=7))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO rooms (room_code, file_name, expiry_time, plan) VALUES (?, ?, ?, ?)',
                     (room_code, file.filename, expiry, plan))
        conn.commit()
        conn.close()

        # 8. Clean up temp audio
        os.remove(temp_audio_path)

        return jsonify({
            "message": "File secured! 🔥",
            "room_code": room_code,
            "expires_at": expiry.strftime("%Y-%m-%d %H:%M:%S")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)