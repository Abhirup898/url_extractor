from flask import Flask, request, jsonify
import requests
import fitz  # PyMuPDF
from io import BytesIO
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/extract_pdf_text', methods=['POST'])
def extract_pdf_text():
    try:
        data = request.json
        pdf_url = data.get("url")
        
        if not pdf_url:
            return jsonify({"error": "URL is required"}), 400
        
        headers = {"User-Agent": "Mozilla/5.0"}  # Add headers to avoid blocking
        response = requests.get(pdf_url, headers=headers, stream=True)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch PDF"}), 400
        
        pdf_bytes = BytesIO(response.content)
        
        # Extract text from the PDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        extracted_text = "\n".join(page.get_text("text") for page in doc if page.get_text("text"))
        
        return jsonify({"text": extracted_text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/extract_web_text', methods=['POST'])
def extract_web_text():
    try:
        data = request.json
        page_url = data.get("url")
        
        if not page_url:
            return jsonify({"error": "URL is required"}), 400

        headers = {"User-Agent": "Mozilla/5.0"}  # Avoid blocking by some servers
        response = requests.get(page_url, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch the webpage"}), 400
        
        soup = BeautifulSoup(response.text, "html.parser")
        extracted_text = soup.get_text(separator="\n", strip=True)  # Extract readable text
        
        return jsonify({"text": extracted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
