import torch
import whisper
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os
import pdfplumber
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from googletrans import Translator
from werkzeug.utils import secure_filename
import wikipediaapi
import urllib.parse
import spacy
from summa import summarizer
import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import fitz 

app = Flask(__name__)

#  Allow credentials & all origins
CORS(app, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000" 
    response.headers["Access-Control-Allow-Credentials"] = "true" 
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'CIP',
    'port': 3307
}

try:
    test_conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Connected successfully!")
    test_conn.close()
except Exception as e:
    print("❌ Connection failed:", e)

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Whisper model for audio transcription
whisper_model = whisper.load_model("tiny")

# Create folders for file uploads and summaries
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "summaries"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load LongT5 model for text summarization
model_name = "google/long-t5-tglobal-base"
summarization_model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

translator = Translator()

print("Models loaded successfully!")


#  Function to summarize text Abstractive
def summarize_text(text, summary_level=0.5):
    if not text.strip():
        return "No content to summarize."

    summary_level = max(0.1, min(1.0, summary_level)) 

    inputs = tokenizer(text, return_tensors="pt", max_length=2048, truncation=True).to(device)
    max_output_length = int(len(inputs.input_ids[0]) * summary_level)
    min_output_length = max(30, int(max_output_length * 0.7))

    summary_ids = summarization_model.generate(
        inputs.input_ids,
        max_length=max_output_length,
        min_length=min_output_length,
        length_penalty=0.3,
        num_beams=8,
        repetition_penalty=2.0,
        no_repeat_ngram_size=3,
        early_stopping=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

nlp = spacy.load("en_core_web_sm")

def spacy_tokenizer(text):
    """Tokenizes text into sentences using spaCy."""
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

def summarize_text_extractive(text, summary_level=0.5):
    """Performs extractive summarization using TextRank."""
    if not text.strip():
        return "No content to summarize."

    summary = summarizer.summarize(text, ratio=summary_level)  
    return summary if summary.strip() else "⚠️ Unable to generate summary!"

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if not page_text:
                    img = page.to_image().original
                    page_text = pytesseract.image_to_string(img)

                text += page_text + "\n"

        return text.strip() if text else None
    except Exception as e:
        return None


def save_summary_to_pdf(summary, output_pdf_path):
    try:
        doc = fitz.open()  # Create a new PDF document
        page = doc.new_page()  # Create a new page
        page.insert_text((50, 50), summary)  # Insert summarized text
        doc.save(output_pdf_path)  # Save the summary as a PDF
        doc.close()
    except Exception as e:
        print(f"Error saving summary to PDF: {e}")
        
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "")
    summary_level = float(data.get("summary_level", 0.5))
    summaryType = data.get("summaryType", "").lower()

    if not text:
        return jsonify({"error": "No text provided!"}), 400

    if summaryType == "abstractive":
        summary = summarize_text(text, summary_level)  
    elif summaryType == "extractive":
        summary = summarize_text_extractive(text, summary_level)  
    else:
        return jsonify({"error": "Invalid summary type! Choose 'abstractive' or 'extractive'."}), 400

    return jsonify({"summary": summary})

@app.route("/summarize_file", methods=["POST"])
def summarize_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["file"]
    summary_level = float(request.form.get("summary_level", 0.5))
    summary_type = request.form.get("summaryType", "extractive").lower()

    if file.filename == "":
        return jsonify({"error": "No file selected!"}), 400

    filename = secure_filename(file.filename)
    file_ext = filename.split(".")[-1].lower()
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    text = None
    if file_ext == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif file_ext == "pdf":
        text = extract_text_from_pdf(file_path)  # Extract text from PDF
    else:
        return jsonify({"error": "Unsupported file type! Only .txt and .pdf allowed."}), 400

    if not text or text.strip() == "":
        return jsonify({"error": "Could not extract text from the file!"}), 400

    if summary_type == "abstractive":
        summary = summarize_text(text, summary_level)  # Call Abstractive summarization
    elif summary_type == "extractive":
        summary = summarize_text_extractive(text, summary_level)  # Call Extractive summarization
    else:
        return jsonify({"error": "Invalid summary type! Choose 'abstractive' or 'extractive'."}), 400

    summary_filename = f"summary_{filename}"
    summary_path = os.path.join(OUTPUT_FOLDER, summary_filename)

    if file_ext == "txt":
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
    elif file_ext == "pdf":
        save_summary_to_pdf(summary, summary_path)  # Use a helper function

    return jsonify({
        "text": text,
        "summary": summary,
        "download_url": f"/download_summary/{summary_filename}"
    })

#  API for downloading summarized file
@app.route("/download_summary/<filename>", methods=["GET"])
def download_summary(filename):
    summary_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(summary_path):
        return send_file(summary_path, as_attachment=True)
    return jsonify({"error": "Summary file not found!"}), 404


#  API for transcribing audio files (`.mp3`)
@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(file_path)

    print("\nTranscribing audio... Please wait...")
    result = whisper_model.transcribe(file_path)
    
    transcript = result["text"]
    return jsonify({"transcript": transcript})


#  API for summarizing audio files (`.mp3`)
@app.route("/audio_summarize", methods=["POST"])
def audio_summarize():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(file_path)

    print("\nTranscribing audio... Please wait...")
    result = whisper_model.transcribe(file_path)

    transcript = result["text"]
    summary = summarize_text_extractive(transcript, 0.5) 

    return jsonify({"transcript": transcript, "summary": summary})


@app.route("/translate", methods=["OPTIONS", "POST"])
def translate_text():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        target_lang = data.get("language", "en")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        sentences = text.split(". ")
        translated_sentences = []
        detected_languages = []

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                detected_lang = translator.detect(sentence).lang
                detected_languages.append({sentence: detected_lang})

                if detected_lang != target_lang:
                    translated_text = translator.translate(sentence, src=detected_lang, dest=target_lang).text
                else:
                    translated_text = sentence
                
                translated_sentences.append(translated_text)

        translated_output = ". ".join(translated_sentences)

        return jsonify({
            "original_text": text,
            "translated_text": translated_output,
            "detected_languages": detected_languages
        })

    except Exception as e:
        return jsonify({"translated_text": "Translation failed", "error": str(e)}), 500
    

@app.route("/save_history", methods=["POST"])
def save_history():
    try:
        data = request.json
        print("Received data:", data)  
        input_text = data.get("text", "").strip()
        output_summ = data.get("summary", "").strip()
        email = data.get("email", "").strip()

        if not input_text or not output_summ or not email:
            return jsonify({"error": "Missing input, summary, or email!"}), 400

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = "INSERT INTO Text_summ_history (input_text, output_summ, created_at, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (input_text, output_summ, datetime.now(), email))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Summary saved successfully!"})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/get_history", methods=["GET"])
def get_history():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)  
        email = request.args.get("email", "").strip()
        print("Received email:", email) 

        if not email:
            return jsonify({"error": "Email parameter is required!"}), 400

        cursor.execute("SELECT * FROM text_summ_history WHERE email = %s ORDER BY created_at DESC", (email,))
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(data)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    mobile = data.get("mobile")
    password = data.get("password")

    if not (username and email and mobile and password):
        return jsonify({"error": "All fields are required!"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, mobile, password) VALUES (%s, %s, %s, %s)",
            (username, email, mobile, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not (email and password):
        return jsonify({"error": "Email and password required!"}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            return jsonify({"message": "Login successful!"})
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except mysql.connector.Error as err:
        print("Database error:", err)  # 👈 Add this
        return jsonify({"error": str(err)}), 500


#  Start the Flask server
if __name__ == "__main__":
    app.run(debug=True, port=5000)