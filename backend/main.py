# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from utils.pdf_reader import extract_text_from_file
from utils.summarizer import generate_summary
from utils.qa_module import answer_question
from utils.quiz_module import generate_quiz, evaluate_answers

print(">>> Running backend.main")

load_dotenv()

app = FastAPI()

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    document: str

class ChallengeRequest(BaseModel):
    document: str

class EvaluateRequest(BaseModel):
    document: str
    user_answers: list[str]

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = extract_text_from_file(file.filename, content)
        summary = generate_summary(text)
        return {"text": text, "summary": summary}
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}


@app.post("/ask")
async def ask_question(req: QuestionRequest):
    answer, justification = answer_question(req.question, req.document)
    return {"answer": answer, "justification": justification}

@app.post("/challenge")
async def challenge_me(req: ChallengeRequest):
    questions = generate_quiz(req.document)
    return {"questions": questions}

@app.post("/evaluate")
async def evaluate(req: EvaluateRequest):
    results = evaluate_answers(req.document, req.user_answers)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)