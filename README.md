# AudioShield

### Secure Audio-Keyed File Sharing System

![React](https://img.shields.io/badge/Frontend-React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=flat-square&logo=flask)
![Postgres](https://img.shields.io/badge/Database-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Storage-Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![AES-GCM](https://img.shields.io/badge/Encryption-AES--GCM-brightgreen?style=flat-square)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat-square&logo=render&logoColor=white)
![Vercel](https://img.shields.io/badge/Deployed-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

AudioShield is a full-stack web application that replaces traditional passwords with **audio files as cryptographic keys**, enabling secure, passwordless file sharing using AES-GCM authenticated encryption. The application is deployed as a production system with a cloud-hosted backend, database, and object storage.

---

## Table of Contents

- [The Concept](#the-concept)
- [How It Works](#how-it-works)
- [System Architecture](#system-architecture)
- [Security Design](#security-design)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Auto Cleanup](#auto-cleanup)
- [Important Notes](#important-notes)
- [Future Roadmap](#future-roadmap)
- [Author](#author)
- [License](#license)

---

## The Concept

Traditional passwords are short, memorable, and therefore brute-forceable. AudioShield replaces the password with an audio file — a data source with millions of bytes of entropy that is impractical to guess or brute-force.

- The sender uploads a target file along with an audio file.
- The audio file's raw bytes are hashed using SHA-256 to derive a 256-bit encryption key.
- The target file is encrypted using AES-GCM and stored.
- A unique Room Code and QR code are generated for retrieval.
- The receiver uploads the exact same audio file to derive the same key and decrypt the file.

Even a single-byte difference in the audio file produces a completely different SHA-256 hash, making decryption mathematically impossible without the correct audio.

---

## How It Works

**1. Upload (Sender)**
- User uploads a file and a "key" audio file via the React frontend.
- The Flask backend reads the audio bytes and computes `SHA-256(audio_bytes)` to derive a 256-bit key.
- The file is encrypted using AES-GCM with a randomly generated 12-byte nonce.
- The encrypted file is uploaded to Supabase Storage.
- A room record (room code, file name, expiry time) is inserted into the PostgreSQL database.
- A Room Code and QR code are returned to the sender.

**2. Sharing**
- The sender shares the Room Code (or QR code) and the original audio file with the receiver through a trusted channel.

**3. Download (Receiver)**
- The receiver enters the Room Code and uploads the same audio file.
- The backend re-derives the key from the audio bytes, fetches the encrypted file from Supabase Storage, and attempts AES-GCM decryption.
- If the audio matches, the file is decrypted and served. If it doesn't, decryption fails and access is denied.

**4. Expiry**
- Rooms and their associated encrypted files automatically expire and are deleted after 24 hours.

---

## System Architecture

```
┌─────────────┐        HTTPS        ┌──────────────┐
│   Frontend   │ ───────────────────▶│   Backend    │
│  (Vercel)    │◀─────────────────── │  (Render)    │
└─────────────┘                     └──────┬───────┘
                                            │
                       ┌────────────────────┼────────────────────┐
                       ▼                                        ▼
              ┌─────────────────┐                     ┌───────────────────┐
              │  Supabase Postgres│                     │ Supabase Storage  │
              │  (room metadata)  │                     │ (encrypted files) │
              └─────────────────┘                     └───────────────────┘
```

- **Frontend** is deployed on Vercel and communicates with the backend over HTTPS.
- **Backend** (Flask) is deployed on Render and handles encryption, decryption, QR generation, and cleanup logic.
- **Database** is a managed PostgreSQL instance on Supabase, accessed via the transaction pooler, storing room metadata (room code, file name, expiry time).
- **Storage** is a private Supabase Storage bucket that holds the AES-GCM encrypted `.enc` files. No plaintext files or audio keys are ever persisted.

---

## Security Design

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
    └── Authentication Tag
    │
    ▼
Stored as .enc file in Supabase Storage
```

AudioShield follows a zero-knowledge principle: the server never stores the original audio file or the derived key. Only the encrypted `.enc` blob (nonce + ciphertext + auth tag) is persisted, and it is deleted automatically after 24 hours.

**Guarantees:**
- **Confidentiality** — file contents are unreadable without the exact audio key.
- **Integrity** — any tampering with the ciphertext is detected via the AES-GCM authentication tag.
- **Authenticity** — decryption only succeeds if the derived key matches the one used for encryption.

---

## Features

- Passwordless encryption — the audio file is the only key
- AES-GCM authenticated encryption (confidentiality + integrity in one primitive)
- QR code generation for convenient sharing
- Automatic file and metadata cleanup after 24 hours
- Support for uploads up to 50MB
- Cloud-native deployment across frontend, backend, database, and storage
- Responsive UI across devices

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Axios |
| Frontend Hosting | Vercel |
| Backend | Python, Flask, Flask-CORS |
| Backend Hosting | Render |
| Encryption | AES-GCM (`cryptography`), SHA-256 (`hashlib`) |
| Database | PostgreSQL (Supabase, transaction pooler) |
| File Storage | Supabase Storage (private bucket) |
| QR Code | `qrcode` library |

---

## Project Structure

```
AudioShield/
│
├── audioshield_backend/
│   ├── app.py               # Flask routes, upload/download logic, cleanup
│   ├── crypto_utils.py      # AES-GCM encryption & decryption
│   ├── database.py          # PostgreSQL connection (Supabase)
│   ├── requirements.txt     # Backend dependencies
│   └── .env                 # DATABASE_URL, SUPABASE_URL, SUPABASE_KEY (gitignored)
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/
│   │   │   └── api.js       # Backend base URL & API calls
│   │   └── App.jsx
│   ├── public/
│   └── package.json
│
└── README.md
```

---

## Installation & Setup

### Prerequisites
- Node.js v18+
- Python 3.9+
- A Supabase project (Postgres database + Storage bucket)

### 1. Clone the Repository
```bash
git clone https://github.com/tushar1121s/AudioShield.git
cd AudioShield
```

### 2. Backend Setup
```bash
cd audioshield_backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in `audioshield_backend/`:
```
DATABASE_URL=<your Supabase Postgres connection string>
SUPABASE_URL=<your Supabase project URL>
SUPABASE_KEY=<your Supabase secret/service_role key>
```

Initialize the database and start the server:
```bash
python database.py
python app.py
```
> Runs at: `http://localhost:5000`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Update `frontend/src/services/api.js` to point to your backend (local or deployed):
```js
const BASE_URL = "http://localhost:5000";
```

> Runs at: `http://localhost:3000`

### 4. Production Deployment
- **Backend** → Deploy to Render (root directory: `audioshield_backend`, build command: `pip install -r requirements.txt`, start command: `python app.py`). Set `DATABASE_URL`, `SUPABASE_URL`, and `SUPABASE_KEY` as environment variables in the Render dashboard.
- **Frontend** → Deploy to Vercel. Update `BASE_URL` in `api.js` to the live Render URL before pushing.
- **Database & Storage** → Managed entirely by Supabase; no additional setup required beyond the initial project and bucket creation.

---

## API Endpoints

### `POST /upload`
Encrypts and stores a file.

| Field | Type | Description |
|---|---|---|
| `file` | form-data | File to protect |
| `audio` | form-data | Audio key file |

**Response:**
```json
{
  "message": "Secured!",
  "room_code": "ABC123",
  "qr_code": "<base64_image>",
  "expires_at": "2026-08-10 19:41:18"
}
```

### `POST /download`
Decrypts and returns the file.

| Field | Type | Description |
|---|---|---|
| `room_code` | string | Room identifier |
| `audio` | form-data | Audio key file |

**Response:** Decrypted file stream, or an error if the audio key or room code is invalid.

### `GET /check-room`
Checks whether a room exists and is still valid.

| Param | Type | Description |
|---|---|---|
| `room` | string | Room code to validate |

---

## Auto Cleanup

A cleanup routine runs before every `/upload` and `/download` request:
- Scans the database for rooms past their expiry time.
- Removes the corresponding encrypted file from Supabase Storage.
- Deletes the room record from PostgreSQL.

Default expiry: **24 hours** from upload time.

---

## Important Notes

- The audio key must be byte-for-byte identical between sender and receiver; even minor re-encoding will change the derived key and cause decryption to fail.
- AudioShield does not store the original file or the audio key at any point — only the AES-GCM encrypted output is persisted, and only temporarily.
- Maximum file size: 50MB.
- All encrypted files and their metadata are permanently deleted after expiry.

---

## Future Roadmap

The current version is a functional end-to-end deployment. Planned improvements to move toward a production-grade, full-stack application:

**Backend**
- Migrate from Flask to FastAPI for async request handling and better concurrency under load.
- Add proper API rate limiting and request validation.
- Introduce structured logging and error monitoring.

**Authentication & User Accounts**
- User login/signup (email or OAuth-based).
- Per-user file history dashboard — view past uploads, room codes, and expiry status.
- Role-based access for shared/team rooms.

**Storage & Scalability**
- Evaluate migration to AWS (S3 + RDS + EC2/ECS) for tighter integration and reduced cross-service latency at scale.
- Configurable file expiry per upload instead of a fixed 24-hour window.
- Support for larger file sizes via chunked/multipart uploads.

**Frontend & UX**
- Full UI redesign for consistent experience across mobile and desktop.
- Progressive Web App (PWA) support for installable mobile experience.
- Real-time upload/decryption progress indicators.
- Dark mode and accessibility improvements.

**Security**
- Audio fingerprinting to tolerate minor re-encoding of the key audio (e.g., format or bitrate changes) while preserving security guarantees.
- Optional multi-factor key derivation (audio + PIN).
- Audit logging for room access attempts.

**Infrastructure**
- CI/CD pipeline for automated testing and deployment.
- Staging environment separate from production.
- Eliminate Render free-tier cold starts via a paid tier or alternative always-on hosting once the project moves toward production use.

---

## Author

**Tushar Kumar**
3rd Year B.Tech, Full-Stack Developer

---

## Why This Project Stands Out

Unlike typical CRUD projects, AudioShield:

- Uses audio as an actual cryptographic primitive rather than a novelty feature.
- Implements AES-GCM authenticated encryption correctly, including nonce handling and key derivation.
- Runs on a real cloud architecture — separate frontend, backend, database, and storage services communicating in production.
- Includes production-relevant features such as automatic expiry, cleanup, and QR-based sharing.
- Demonstrates practical understanding of both applied cryptography and full-stack deployment.

---

## License

This project is licensed under the [MIT License](LICENSE).