# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit UI Configuration
st.set_page_config(page_title="🧠 Smart Document Assistant", layout="centered")
st.title("🧠 Smart Assistant for Document Summarization and Reasoning")

# Session state to persist document content if needed
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

# Upload File Section
st.header("📄 Upload Your Document")
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Reading and processing your document..."):
        try:
            # Send file with correct tuple (filename, content, MIME type)
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            response = requests.post("http://localhost:8000/upload", files=files)

            if response.status_code == 200:
                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.session_state.doc_text = data["text"]
                    st.subheader("📌 Auto Summary")
                    st.write(data["summary"])

                    # Select Mode
                    st.subheader("💡 Choose a Mode")
                    mode = st.radio("Select interaction mode:", ["Ask Anything", "Challenge Me"])

                    if mode == "Ask Anything":
                        question = st.text_input("Ask a question about the document:")
                        if question:
                            with st.spinner("Thinking..."):
                                answer_response = requests.post("http://localhost:8000/ask", json={
                                    "question": question,
                                    "document": st.session_state.doc_text
                                })
                                if answer_response.status_code == 200:
                                    result = answer_response.json()
                                    st.markdown("**Answer:**")
                                    st.write(result["answer"])
                                    st.markdown(f"_Justification: {result['justification']}_")
                                else:
                                    st.error("Error processing the question.")

                    elif mode == "Challenge Me":
                        st.write("Generating logic-based questions from the document...")
                        quiz_response = requests.post("http://localhost:8000/challenge", json={"document": st.session_state.doc_text})
                        if quiz_response.status_code == 200:
                            quiz_data = quiz_response.json()
                            user_answers = []

                            for i, q in enumerate(quiz_data["questions"]):
                                user_input = st.text_input(f"Q{i+1}: {q}", key=f"quiz_q{i}")
                                user_answers.append(user_input)

                            if st.button("Submit Answers"):
                                evaluation_response = requests.post("http://localhost:8000/evaluate", json={
                                    "document": st.session_state.doc_text,
                                    "user_answers": user_answers
                                })
                                if evaluation_response.status_code == 200:
                                    feedback = evaluation_response.json()
                                    st.subheader("📝 Feedback")
                                    for i, f in enumerate(feedback["results"]):
                                        st.markdown(f"**Q{i+1}:** {f['question']}")
                                        st.markdown(f"- Your Answer: {f['user_answer']}")
                                        st.markdown(f"- Correctness: {f['correct']}")
                                        st.markdown(f"- Justification: _{f['justification']}_")
                                else:
                                    st.error("Could not evaluate answers.")
                        else:
                            st.error("Error generating quiz questions.")
            else:
                st.error(f"Server error: {response.status_code}")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
