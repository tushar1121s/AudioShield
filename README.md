# 🛡️ AudioShield
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=38B2AC&center=true&vCenter=true&width=500&lines=%F0%9F%9B%A1%EF%B8%8F+AUDIOSHIELD;Secure+Audio-Keyed+Encryption;AES-GCM+Protected+Sharing;Built+by+Tushar+Kumar"/>
</p>
<p align="center">
  <img src="https://img.shields.io/github/stars/tushar1121s/AudioShield?style=for-the-badge&color=38B2AC"/>
  <img src="https://img.shields.io/github/forks/tushar1121s/AudioShield?style=for-the-badge&color=38B2AC"/>
  <img src="https://img.shields.io/github/repo-size/tushar1121s/AudioShield?style=for-the-badge&color=38B2AC"/>
</p>

<p align="center">
  <a href="#-the-idea"><img src="https://img.shields.io/badge/💡_The_Idea-38B2AC?style=for-the-badge&logoColor=white" /></a>
  <a href="#-how-it-works"><img src="https://img.shields.io/badge/🧠_How_It_Works-38B2AC?style=for-the-badge&logoColor=white" /></a>
  <a href="#-installation--setup"><img src="https://img.shields.io/badge/⚙️_Installation-38B2AC?style=for-the-badge&logoColor=white" /></a>
  <a href="#-security-design"><img src="https://img.shields.io/badge/🔐_Security-38B2AC?style=for-the-badge&logoColor=white" /></a>
  <a href="#-roadmap"><img src="https://img.shields.io/badge/🗺️_Roadmap-38B2AC?style=for-the-badge&logoColor=white" /></a>
</p>

---
### Secure Audio-Keyed File Sharing System

![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=flat-square&logo=flask)
![AES-GCM](https://img.shields.io/badge/Encryption-AES--GCM-brightgreen?style=flat-square)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> AudioShield is a full-stack web application that replaces passwords with **audio files as cryptographic keys** — enabling secure, passwordless file sharing using real-world AES-GCM encryption.

---

## 💡 The Concept

> [!TIP]
> **AudioShield flips the script on passwords.** Instead of a 12-character string that can be brute-forced, we use the **millions of bytes** in an audio file to generate a 256-bit cryptographic key.

> [!IMPORTANT]
> **No Audio = No Access.** Even a 1-byte difference in the "Key" audio file will result in a completely different SHA-256 hash, making decryption mathematically impossible.

**AudioShield flips this entirely:**

- 🎵 Upload a file + an audio file
- 🔑 The audio becomes your encryption key (via SHA-256)
- 🛡️ File is encrypted with AES-GCM
- 📦 A Room Code is generated for the receiver
- 🔽 Receiver uploads the **same audio file** → gets the decrypted file

> No passwords. No accounts. Just audio.

---

## 🧠 How It Works
```mermaid
sequenceDiagram
    autonumber
    participant U as User (Sender)
    participant F as React UI
    participant B as Flask API
    participant D as SQLite DB

    U->>F: Uploads File + Audio
    F->>B: POST /upload
    Note over B: SHA-256(Audio) = 256-bit Key
    Note over B: AES-GCM Encrypts File
    B->>D: Logs Room Metadata
    B->>F: Returns Code + QR
    F->>U: Displays Success

### 🔼 Upload — Sender Side

1. User uploads a **file** and an **audio file**
2. Backend reads audio → raw bytes
3. `SHA-256(audio_bytes)` → 256-bit encryption key
4. File is encrypted using **AES-GCM** with a random 12-byte nonce
5. Encrypted file is stored on the server
6. A unique **Room Code** and **QR Code** are returned

---

### 🔗 Sharing Phase

The sender shares two things via a trusted channel:
- The **Room Code** or **QR Code**
- The **original audio file** (exact copy)

---

### 🔽 Download — Receiver Side

1. Receiver enters the Room Code (or scans QR)
2. Uploads the same audio file
3. Backend regenerates the key from audio bytes
4. Extracts nonce → decrypts file using AES-GCM
```
✅ Audio matches  →  File downloaded successfully
❌ Audio differs  →  Access denied
```

---
## 🔒 Security Architecture

AudioShield implements **Authenticated Encryption with Associated Data (AEAD)** via the AES-GCM algorithm.

$$Key = \text{SHA-256}(\text{Audio Bytes})$$
$$Ciphertext = \text{AES-GCM}_{Key, Nonce}(\text{Plaintext})$$

> [!CAUTION]
> We follow the **"Zero-Knowledge"** principle. The server never stores the original audio or the derived key. It only stores the `.enc` file and the random 12-byte nonce.


## ✨ Features

- 🔐 **Passwordless encryption** — audio file is the only key
- 🛡️ **AES-GCM** authenticated encryption (confidentiality + integrity)
- 📷 **QR Code** generation for easy sharing
- 🧹 **Auto file cleanup** after 24 hours
- ⚡ **50MB** file upload support
- 📱 **Responsive UI** — React + Tailwind CSS

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React (Vite), CSS, Axios |
| Backend | Python, Flask, Flask-CORS |
| Encryption | AES-GCM (`cryptography`), SHA-256 (`hashlib`) |
| QR Code | `qrcode` library |
| Database | SQLite |

---

## 📁 Project Structure
```
AudioShield/
│
├── backend/
│   ├── app.py              # Flask routes & API logic
│   ├── crypto_utils.py     # AES-GCM encryption & decryption
│   ├── database.py         # SQLite setup & queries
│   ├── database.db         # Local database file
│   └── uploads/            # Encrypted file storage
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   └── App.jsx
│   ├── public/
│   └── package.json
│
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Node.js v18+
- Python 3.9+
- pip

---

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/tushar1121s/audioshield.git
cd audioshield
```

---

### 2️⃣ Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-cors cryptography qrcode

# Initialize the database
python database.py

# Start the server
python app.py
```

> Runs at: `http://localhost:5000`

---

### 3️⃣ Frontend Setup
```bash
cd frontend

npm install
npm run dev
```

> Runs at: `http://localhost:3000`

---

## 🔐 Security Design
```
Audio File
    │
    ▼
SHA-256(audio_bytes)
    │
    ▼
256-bit Encryption Key
    │
    ▼
AES-GCM Encrypt
    ├── Random 12-byte Nonce
    ├── Ciphertext
    └── Auth Tag
    │
    ▼
Stored as .enc file (nonce + ciphertext)
```

**What this guarantees:**
- ✅ Confidentiality — unreadable without the correct audio file
- ✅ Integrity — any tampering is detected instantly
- ✅ Authenticity — AES-GCM tag validates the decryption

---

## 📡 API Endpoints

### `POST /upload`
Encrypts and stores a file.

| Field | Type | Description |
|-------|------|-------------|
| `file` | form-data | File to protect |
| `audio` | form-data | Audio key file |

**Response:**
```json
{
  "room_code": "ABC123",
  "qr_code": "<base64_image>"
}
```

---

### `POST /download`
Decrypts and returns the file.

| Field | Type | Description |
|-------|------|-------------|
| `room_code` | string | Room identifier |
| `audio` | form-data | Audio key file |

**Response:** Decrypted file stream, or `403 Access Denied`

---

### `GET /check-room`
Checks if a room exists.

| Param | Type | Description |
|-------|------|-------------|
| `room_code` | string | Room to validate |

---

## 🧹 Auto Cleanup

A cleanup routine runs **before every request**:
- Scans all stored files for expiry
- Deletes files from disk
- Removes records from the database

> Expiry: **24 hours** from upload time

---

## ⚠️ Important Notes

- Audio must be **byte-for-byte identical** — even minor edits cause decryption to fail
- AudioShield does **not** store your original file or audio key — only the encrypted output
- Max file size: **50MB**
- All files are **permanently deleted** after 24 hours

---

## 🗺️ Future Roadmap

- [ ] Cloud deployment (Render + Vercel)
- [ ] MongoDB for scalable storage
- [ ] AWS S3 / Cloudinary for file hosting
- [ ] Audio fingerprinting (tolerance for minor audio edits)
- [ ] User authentication & file history dashboard

---

## 👨‍💻 Author

**Tushar Kumar** — 3rd Year B.Tech, Full-Stack Developer

---

## ⭐ Why This Project Stands Out

Unlike typical CRUD projects, AudioShield:

- Uses **audio as a real cryptographic primitive** — not just a gimmick
- Implements **production-grade AES-GCM encryption** from scratch
- Combines security + usability with **QR-based sharing**
- Includes real-world features like **auto expiry and cleanup**
- Demonstrates deep understanding of **cryptography concepts**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).