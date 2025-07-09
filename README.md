# Text & Audio Summarization API

A full‑stack project that provides **abstractive and extractive summarization**, **audio transcription**, **translation** and **history management** through a Flask REST API.  A minimal React front‑end lives in `f‑end/text-summarizer-frontend`.

---

## ✨ Features

| Capability                                    | Endpoint                                 | Notes                                                             |
| --------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------- |
| Text summarization (abstractive / extractive) | `POST /summarize`                        | JSON body with `text`, `summaryType` and optional `summary_level` |
| File summarization (`.txt`, `.pdf`)           | `POST /summarize_file`                   | Multipart upload, returns download link                           |
| Audio transcription (`.mp3`)                  | `POST /transcribe`                       | Whisper Tiny model                                                |
| Audio summarization (`.mp3`)                  | `POST /audio_summarize`                  | Two‑stage TextRank extractive summary                             |
| Translation                                   | `POST /translate`                        | Per‑sentence detection & translate with *googletrans*             |
| Save / fetch summary history                  | `POST /save_history`, `GET /get_history` | Stores to MySQL (`Text_summ_history`)                             |
| Auth                                          | `POST /signup`, `POST /login`            | Passwords hashed with Werkzeug                                    |

---

## 🏗  Tech Stack

* **Backend:** Flask 2.x, Flask‑CORS, MySQL‑connector‑python
* **NLP / ML:**

  * Google *Long‑T5* (`google/long-t5-tglobal-base`)  → abstractive summary
  * *Whisper Tiny*  → audio transcription
  * spaCy (`en_core_web_sm`)  → tokenisation / NER
  * NLTK, ROUGE, BLEU, BERTScore  → evaluation metrics
  * summa (TextRank)  → extractive summary
* **OCR / PDF:** pdfplumber, PyMuPDF (*fitz*), pytesseract
* **Front‑end (optional demo):** React (vite) in `/f-end/text-summarizer-frontend`

---

## 📂 Project Structure (server side)

```
TextSum/
├─ app.py                # main Flask server (this file)
├─ accuracy.py           # metric helpers
├─ uploads/              # temp file uploads
├─ summaries/            # generated summaries for download
├─ env/ | venv/          # virtual‑environment (ignored)
├─ f-end/                # React front‑end & Node assets
└─ requirements.txt      # Python deps (see below)
```

> **Note:** `uploads/`, `summaries/`, `env/`, `venv/`, and all `node_modules/` folders are ignored via `.gitignore`.

---

## 🖥️  Local Setup

### 1  Clone & create virtual environment

```bash
# Clone your fork
$ git clone https://github.com/<you>/TextSum.git
$ cd TextSum

# Create & activate venv (Windows)
$ python -m venv venv
$ venv\Scripts\activate
```

### 2  Install Python dependencies

```bash
(venv) $ pip install -r requirements.txt
# or build manually
(venv) $ pip install torch transformers whisper googletrans==4.0.0-rc1 \
           flask flask-cors pdfplumber pytesseract pillow wikipedia-api spacy summa \
           mysql-connector-python rouge-score nltk bert-score pymupdf

# Download spaCy model
(venv) $ python -m spacy download en_core_web_sm
```

### 3  MySQL

1. Create database `CIP` and tables:

   ```sql
   CREATE DATABASE CIP;
   USE CIP;

   CREATE TABLE users (
     id INT AUTO_INCREMENT PRIMARY KEY,
     username VARCHAR(50), email VARCHAR(100) UNIQUE,
     mobile VARCHAR(15), password VARCHAR(255)
   );

   CREATE TABLE text_summ_history (
     id INT AUTO_INCREMENT PRIMARY KEY,
     input_text LONGTEXT, output_summ LONGTEXT,
     created_at DATETIME, email VARCHAR(100)
   );
   ```
2. Update credentials in **`DB_CONFIG`** inside `app.py` if needed.

### 4  Run the server

```bash
(venv) $ python app.py
# → Server running at http://localhost:5000
```

### 5  (Option) Front‑end quick start

```bash
$ cd f-end/text-summarizer-frontend
$ npm install
$ npm run dev            # runs on http://localhost:5173
```

---


## 🎯  Example Requests

### 1  Text → Abstractive Summary

```http
POST /summarize
Content‑Type: application/json

{
  "text": "<your long article>",
  "summaryType": "abstractive",
  "summary_level": 0.4
}
```

### 2  PDF File → Extractive Summary

```bash
curl -F "file=@paper.pdf" \
     -F "summary_level=0.3" \
     -F "summaryType=extractive" \
     http://localhost:5000/summarize_file
```

### 3  Audio (.mp3) → Summary

```bash
curl -F "file=@lecture.mp3" http://localhost:5000/audio_summarize
```

---

## 📜  License

CEG © 2025 Nagarjun M / CEG Anna University

