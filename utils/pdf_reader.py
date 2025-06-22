import io
import pdfplumber

def extract_text_from_file(filename, content):
    try:
        if filename.lower().endswith(".pdf"):
            text = ""
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()

        elif filename.lower().endswith(".txt"):
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                raise RuntimeError("Unable to decode the text file. Please ensure it's UTF-8 encoded.")

        else:
            raise ValueError(f"Unsupported file format: {filename}")

    except Exception as e:
        raise RuntimeError(f"Failed to read file '{filename}': {e}")
