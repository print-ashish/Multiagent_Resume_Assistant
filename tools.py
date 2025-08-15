import PyPDF2

def read_pdf() -> str:
    """Reads text from a PDF file and returns it as a string."""
    text = ""
    file_path ="resumes\\resume.pdf"
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        return f"Error reading PDF: {e}"
    return text



# text = read_pdf("resumes\\ashish_resume.pdf")
# text = read_pdf()
# print(text)