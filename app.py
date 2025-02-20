import requests
from PyPDF2 import PdfReader
from io import BytesIO
import docx
from flask import Flask, request, jsonify

app = Flask(__name__)

def extract_pdf_text(url):
    # Fetch PDF from the URL
    response = requests.get(url)
    file = BytesIO(response.content)
    reader = PdfReader(file)
    
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    return text

def extract_docx_text(url):
    # Fetch Word document from the URL
    response = requests.get(url)
    file = BytesIO(response.content)
    doc = docx.Document(file)
    
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    
    return text

@app.route('/extract-text', methods=['POST'])
def extract_text_from_document():
    # Get the document URL from the request
    data = request.get_json()
    document_url = data.get("url")
    
    if not document_url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Check file extension and decide on extraction method
    if document_url.lower().endswith(".pdf"):
        text = extract_pdf_text(document_url)
    elif document_url.lower().endswith(".docx"):
        text = extract_docx_text(document_url)
    else:
        return jsonify({"error": "Unsupported file type"}), 400
    
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(debug=True)
