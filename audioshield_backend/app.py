from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os, uuid, sqlite3, hashlib
from datetime import datetime, timedelta
from crypto_utils import generate_key_from_bytes, encrypt_data, decrypt_data

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    # Yeh line jadoo hai! Isse hum room['file_name'] likh payenge
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        audio = request.files['audio']
        
        # Audio bytes read karo aur Hash print karo
        audio_bytes = audio.read()
        audio_hash = hashlib.sha256(audio_bytes).hexdigest()
        print(f"\n[UPLOAD] Audio Hash: {audio_hash}") # Yeh terminal mein dikhega

        key = generate_key_from_bytes(audio_bytes)
        encrypted_content = encrypt_data(file.read(), key)

        room_code = str(uuid.uuid4())[:8].upper()
        file_path = os.path.join(UPLOAD_FOLDER, f"{room_code}.enc")
        
        with open(file_path, 'wb') as f:
            f.write(encrypted_content)

        expiry = datetime.now() + timedelta(days=1)
        conn = get_db_connection()
        conn.execute('INSERT INTO rooms (room_code, file_name, expiry_time) VALUES (?, ?, ?)',
                     (room_code, file.filename, expiry))
        conn.commit()
        conn.close()

        return jsonify({"message": "Secured!", "room_code": room_code}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['POST'])
def download_file():
    try:
        room_code = request.form.get('room_code')
        audio = request.files.get('audio')

        # Audio bytes read karo aur Hash print karo
        audio_bytes = audio.read()
        audio_hash = hashlib.sha256(audio_bytes).hexdigest()
        print(f"[DOWNLOAD] Audio Hash: {audio_hash}") # Yeh match hona chahiye!

        conn = get_db_connection()
        room = conn.execute('SELECT * FROM rooms WHERE room_code = ?', (room_code,)).fetchone()
        conn.close()

        if not room: return jsonify({"error": "Invalid room"}), 404

        key = generate_key_from_bytes(audio_bytes)
        with open(os.path.join(UPLOAD_FOLDER, f"{room_code}.enc"), 'rb') as f:
            decrypted_content = decrypt_data(f.read(), key)

        temp_path = f"decrypted_{room['file_name']}"
        with open(temp_path, 'wb') as f:
            f.write(decrypted_content)

        return send_file(temp_path, as_attachment=True)
    except Exception as e:
        print(f"!!! DECRYPTION ERROR: {str(e)}") # Real error terminal mein dikhega
        return jsonify({"error": "Wrong audio key!"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)