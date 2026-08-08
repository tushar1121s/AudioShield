from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os, uuid, qrcode, io, base64
from datetime import datetime, timedelta
from psycopg2.extras import RealDictCursor
from database import get_connection
from crypto_utils import generate_key_from_bytes, encrypt_data, decrypt_data

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- CONFIG ---
FRONTEND_URL = "https://audio-shield.vercel.app"
MAX_FILE_SIZE_MB = 50

def get_db_connection():
    conn = get_connection()
    return conn

# --- FEATURE: AUTO-CLEANUP ---
def cleanup_expired_files():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    now = datetime.now()
    cursor.execute('SELECT room_code FROM rooms WHERE expiry_time < %s', (now,))
    expired_rooms = cursor.fetchall()

    for room in expired_rooms:
        code = room['room_code']
        file_path = os.path.join(UPLOAD_FOLDER, f"{code}.enc")
        if os.path.exists(file_path):
            os.remove(file_path)
        cursor.execute('DELETE FROM rooms WHERE room_code = %s', (code,))
        print(f"🧹 Cleaned up expired room: {code}")

    conn.commit()
    cursor.close()
    conn.close()

# --- FEATURE: QR GENERATOR ---
def generate_qr_base64(room_code):
    full_url = f"{FRONTEND_URL}/receive?room={room_code}"
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
        if 'file' not in request.files or 'audio' not in request.files:
            return jsonify({"error": "Both file and audio are required!"}), 400

        file = request.files['file']
        audio = request.files['audio']

        if file.filename == '' or audio.filename == '':
            return jsonify({"error": "No file selected!"}), 400

        file_bytes = file.read()
        if len(file_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
            return jsonify({"error": f"File too large! Max {MAX_FILE_SIZE_MB}MB allowed."}), 413

        audio_bytes = audio.read()
        if len(audio_bytes) == 0:
            return jsonify({"error": "Audio file is empty!"}), 400

        key = generate_key_from_bytes(audio_bytes)
        print(f"🔑 Encryption Key: {key.hex()}")
        encrypted_content = encrypt_data(file_bytes, key)

        room_code = str(uuid.uuid4())[:8].upper()
        file_path = os.path.join(UPLOAD_FOLDER, f"{room_code}.enc")
        with open(file_path, 'wb') as f:
            f.write(encrypted_content)

        expiry = datetime.now() + timedelta(days=1)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO rooms (room_code, file_name, expiry_time) VALUES (%s, %s, %s)',
                        (room_code, file.filename, expiry))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Secured! 🔥",
            "room_code": room_code,
            "qr_code": generate_qr_base64(room_code),
            "expires_at": expiry.strftime("%Y-%m-%d %H:%M:%S")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROUTE: DOWNLOAD ---
@app.route('/download', methods=['POST'])
def download_file():
    cleanup_expired_files()
    try:
        room_code = request.form.get('room_code', '').strip().upper()
        audio = request.files.get('audio')

        if not room_code:
            return jsonify({"error": "Room code is required!"}), 400
        if not audio:
            return jsonify({"error": "Audio file is required!"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM rooms WHERE room_code = %s', (room_code,))
        room = cursor.fetchone()
        cursor.close()
        conn.close()

        if not room:
            return jsonify({"error": "Room expired or invalid code!"}), 404

        audio_bytes = audio.read()
        if len(audio_bytes) == 0:
            return jsonify({"error": "Audio file is empty!"}), 400

        key = generate_key_from_bytes(audio_bytes)
        print(f"🔑 Decryption Key: {key.hex()}")

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

# --- ROUTE: CHECK ROOM ---
@app.route('/check-room', methods=['GET'])
def check_room():
    room_code = request.args.get('room', '').strip().upper()
    if not room_code:
        return jsonify({"valid": False, "error": "No room code provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT room_code, file_name, expiry_time FROM rooms WHERE room_code = %s', (room_code,))
    room = cursor.fetchone()
    cursor.close()
    conn.close()

    if not room:
        return jsonify({"valid": False, "error": "Room not found or expired"}), 404

    return jsonify({
        "valid": True,
        "file_name": room['file_name'],
        "expires_at": room['expiry_time'].strftime("%Y-%m-%d %H:%M:%S")
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)