# Smart Assistant for Document Summarization and Reasoning

A multi-modal AI-powered assistant designed to process PDF and TXT files, auto-generate summaries, answer user queries with justifications, and generate and evaluate logic-based quiz questions.

---

## 🚀 Features

* Upload `.pdf` or `.txt` documents
* Get AI-generated summaries using OpenAI
* Ask context-aware questions about the content
* Enter "Challenge Me" mode to test your understanding
* AI-generated questions and AI-evaluated answers with justification

---

## 🧭 Flowchart Diagram

A simple flowchart of how the data flows in this app.
<img src="https://github.com/user-attachments/assets/9bb2edb8-b640-4924-9735-9fe517108984" width="500" height="500"/>

---

## 📁 Folder Structure

```
Smart-Assistant-for-Research-Summarization/
├── backend/
│   └── main.py
├── frontend/
│   └── app.py
├── utils/
│   ├── pdf_reader.py
│   ├── summarizer.py
│   ├── qa_module.py
│   └── quiz_module.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/your-username/Smart-Assistant-for-Research-Summarization.git
cd Smart-Assistant-for-Research-Summarization
```

### 2. Create & Activate Virtual Environment (Optional but Recommended)

```
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate.bat       # Windows
```
> ⚠️ If you're using PowerShell and run into execution policy errors, run this before activating Virtual Environment:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Requirements

```
pip install -r requirements.txt
```

### 4. Set Up Your `.env` File

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```
---

## 🧠 Usage Guide

### Step 1: Run the Backend (FastAPI)

```
uvicorn backend.main:app --reload
```
Server will run at: `http://localhost:8000`

### Step 2: Run the Frontend (Streamlit)

```
streamlit run frontend/app.py
```
This will open a browser tab at: `http://localhost:8501`

---

## 🧪 Challenge Me Mode (How it works)

1. Questions are generated ONCE per document upload.
2. You input your answers.
3. When you hit "Submit Answers" it sends both the **same questions** and your **answers** for evaluation.
4. OpenAI returns correctness and justifications per question.

> ⚠️ Avoid refreshing the app after entering answers, as that resets session state.

---

## 🛠️ Technologies Used

* [Streamlit](https://streamlit.io/) - Frontend interface
* [FastAPI](https://fastapi.tiangolo.com/) - Backend API
* [OpenAI API](https://platform.openai.com/docs) - LLM-based responses
* [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF text extraction
* Python 3.10+

---

## 🚀 Output Screenshots

The screenshots of the AI Assistant can be found in the folder named **_output pics_**.

---

## 🔍 Troubleshooting

* `ModuleNotFoundError: No module named 'dotenv'`

  * Make sure to install `python-dotenv` and activate your virtual environment
* Backend doesn't reload?

  * Restart the Uvicorn process if changing environment variables or code logic
* Questions keep changing?

  * This happens if session state is reset (e.g. app refresh). Avoid refreshing mid-way.

---

## 📄 License

MIT License

---

## 🤝 Contributions

Pull requests are welcome. Please open an issue first to discuss major changes or new features.

---

## ✨ Future Improvements

* PDF highlights support
* Save/export quiz results
* Document memory across sessions
* Support for other LLMs like DeepSeek
