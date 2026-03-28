from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os, uuid, sqlite3, qrcode, io, base64
from datetime import datetime, timedelta
from crypto_utils import generate_key_from_bytes, encrypt_data, decrypt_data

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- CONFIG ---
FRONTEND_URL = "http://localhost:3000"  # Change to your deployed URL later
MAX_FILE_SIZE_MB = 50  # 50MB limit

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- FEATURE: AUTO-CLEANUP (The Janitor) ---
def cleanup_expired_files():
    conn = get_db_connection()
    now = datetime.now()
    expired_rooms = conn.execute('SELECT room_code FROM rooms WHERE expiry_time < ?', (now,)).fetchall()

    for room in expired_rooms:
        code = room['room_code']
        file_path = os.path.join(UPLOAD_FOLDER, f"{code}.enc")
        if os.path.exists(file_path):
            os.remove(file_path)
        conn.execute('DELETE FROM rooms WHERE room_code = ?', (code,))
        print(f"🧹 Cleaned up expired room: {code}")

    conn.commit()
    conn.close()

# --- FEATURE: QR GENERATOR (Fixed - now encodes full URL) ---
def generate_qr_base64(room_code):
    full_url = f"{FRONTEND_URL}/receive?room={room_code}"  # ✅ Full URL now
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(full_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- ROUTE: UPLOAD ---
@app.route('/upload', methods=['POST'])
def upload_file():
    cleanup_expired_files()
    try:
        # Validate files exist
        if 'file' not in request.files or 'audio' not in request.files:
            return jsonify({"error": "Both file and audio are required!"}), 400

        file = request.files['file']
        audio = request.files['audio']

        if file.filename == '' or audio.filename == '':
            return jsonify({"error": "No file selected!"}), 400

        # File size check
        file_bytes = file.read()
        if len(file_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
            return jsonify({"error": f"File too large! Max {MAX_FILE_SIZE_MB}MB allowed."}), 413

        audio_bytes = audio.read()
        if len(audio_bytes) == 0:
            return jsonify({"error": "Audio file is empty!"}), 400

        # Encrypt
        key = generate_key_from_bytes(audio_bytes)
        encrypted_content = encrypt_data(file_bytes, key)

        # Save
        room_code = str(uuid.uuid4())[:8].upper()
        file_path = os.path.join(UPLOAD_FOLDER, f"{room_code}.enc")
        with open(file_path, 'wb') as f:
            f.write(encrypted_content)

        # DB entry
        expiry = datetime.now() + timedelta(days = 1)
        conn = get_db_connection()
        conn.execute('INSERT INTO rooms (room_code, file_name, expiry_time) VALUES (?, ?, ?)',
                     (room_code, file.filename, expiry))
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Secured! 🔥",
            "room_code": room_code,
            "qr_code": generate_qr_base64(room_code),  # ✅ Now has full URL
            "expires_at": expiry.strftime("%Y-%m-%d %H:%M:%S")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROUTE: DOWNLOAD ---
@app.route('/download', methods=['POST'])
def download_file():
    cleanup_expired_files()
    try:
        room_code = request.form.get('room_code', '').strip().upper()  # ✅ Auto uppercase + strip
        audio = request.files.get('audio')

        if not room_code:
            return jsonify({"error": "Room code is required!"}), 400
        if not audio:
            return jsonify({"error": "Audio file is required!"}), 400

        conn = get_db_connection()
        room = conn.execute('SELECT * FROM rooms WHERE room_code = ?', (room_code,)).fetchone()
        conn.close()

        if not room:
            return jsonify({"error": "Room expired or invalid code!"}), 404

        audio_bytes = audio.read()
        if len(audio_bytes) == 0:
            return jsonify({"error": "Audio file is empty!"}), 400

        key = generate_key_from_bytes(audio_bytes)

        enc_path = os.path.join(UPLOAD_FOLDER, f"{room_code}.enc")
        if not os.path.exists(enc_path):
            return jsonify({"error": "File not found on server!"}), 404

        with open(enc_path, 'rb') as f:
            decrypted_content = decrypt_data(f.read(), key)

        return send_file(
            io.BytesIO(decrypted_content),
            as_attachment=True,
            download_name=room['file_name']
        )

    except Exception as e:
        return jsonify({"error": "Wrong audio key or corrupted data!"}), 400

# --- ROUTE: CHECK ROOM (bonus - for frontend validation) ---
@app.route('/check-room', methods=['GET'])
def check_room():
    room_code = request.args.get('room', '').strip().upper()
    if not room_code:
        return jsonify({"valid": False, "error": "No room code provided"}), 400

    conn = get_db_connection()
    room = conn.execute('SELECT room_code, file_name, expiry_time FROM rooms WHERE room_code = ?', (room_code,)).fetchone()
    conn.close()

    if not room:
        return jsonify({"valid": False, "error": "Room not found or expired"}), 404

    return jsonify({
        "valid": True,
        "file_name": room['file_name'],
        "expires_at": room['expiry_time']
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)