from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os, uuid, sqlite3, hashlib, qrcode, io, base64
from datetime import datetime, timedelta
from crypto_utils import generate_key_from_bytes, encrypt_data, decrypt_data

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Dictionary access ke liye
    return conn

# --- FEATURE: AUTO-CLEANUP (The Janitor) ---
def cleanup_expired_files():
    conn = get_db_connection()
    now = datetime.now()
    # Expired rooms dhoondo
    expired_rooms = conn.execute('SELECT room_code FROM rooms WHERE expiry_time < ?', (now,)).fetchall()
    
    for room in expired_rooms:
        code = room['room_code']
        file_path = os.path.join(UPLOAD_FOLDER, f"{code}.enc")
        if os.path.exists(file_path):
            os.remove(file_path) # Storage se delete
        conn.execute('DELETE FROM rooms WHERE room_code = ?', (code,)) # DB se delete
        print(f"🧹 Cleaned up expired room: {code}")
    
    conn.commit()
    conn.close()

# --- FEATURE: QR GENERATOR ---
def generate_qr_base64(room_code):
    # React frontend ka URL yahan aayega (Abhi ke liye sirf room_code)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(room_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.route('/upload', methods=['POST'])
def upload_file():
    cleanup_expired_files() # Har upload se pehle kachra saaf karo
    try:
        file = request.files['file']
        audio = request.files['audio']
        
        audio_bytes = audio.read()
        key = generate_key_from_bytes(audio_bytes)
        
        # File encrypt karo
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

        return jsonify({
            "message": "Secured! 🔥",
            "room_code": room_code,
            "qr_code": generate_qr_base64(room_code),
            "expires_at": expiry.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['POST'])
def download_file():
    cleanup_expired_files() # Download se pehle bhi check karo
    try:
        room_code = request.form.get('room_code')
        audio = request.files.get('audio')

        conn = get_db_connection()
        room = conn.execute('SELECT * FROM rooms WHERE room_code = ?', (room_code,)).fetchone()
        conn.close()

        if not room:
            return jsonify({"error": "Room expired or invalid code!"}), 404

        audio_bytes = audio.read()
        key = generate_key_from_bytes(audio_bytes)
        
        with open(os.path.join(UPLOAD_FOLDER, f"{room_code}.enc"), 'rb') as f:
            decrypted_content = decrypt_data(f.read(), key)

        return send_file(
            io.BytesIO(decrypted_content),
            as_attachment=True,
            download_name=room['file_name']
        )
    except Exception as e:
        return jsonify({"error": "Wrong audio key or corrupted data!"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)