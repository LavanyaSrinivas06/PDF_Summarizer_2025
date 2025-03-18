from flask import Flask, request, render_template, jsonify
import os
from summarizer import extract_text_from_pdf, summarize_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    text = extract_text_from_pdf(file_path)
    summary = summarize_text(text)

    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)