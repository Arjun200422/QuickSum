🧠 Text & Audio Summarization App
A project using Flask and React to:

Summarize text (abstractive & extractive)

Transcribe and summarize audio files (.mp3)

Summarize .pdf and .txt files

Translate text into other languages

Save and view summary history

User login and signup (MySQL)

🚀 How to Run
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/<your-username>/TextSum.git
cd TextSum
2. Setup Virtual Environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
3. MySQL Setup
Create a database CIP and two tables:

sql
Copy
Edit
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  email VARCHAR(100),
  mobile VARCHAR(15),
  password VARCHAR(255)
);

CREATE TABLE text_summ_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  input_text LONGTEXT,
  output_summ LONGTEXT,
  created_at DATETIME,
  email VARCHAR(100)
);
Update your MySQL config in app.py.

4. Run the Flask App
bash
Copy
Edit
python app.py
Runs on: http://localhost:5000

🖥️ Optional: Run Frontend
bash
Copy
Edit
cd f-end/text-summarizer-frontend
npm install
npm run dev
Runs on: http://localhost:5173

✅ Main APIs
/summarize – Summarize text

/summarize_file – Upload .txt or .pdf

/transcribe – Transcribe .mp3

/audio_summarize – Summarize .mp3

/translate – Translate text

/signup, /login – Auth

/save_history, /get_history – Summary history

📌 Notes
Don't upload folders like venv/, env/, node_modules/

Supports GPU if available

👤 Author
Nagarjun M — CEG, Anna University
