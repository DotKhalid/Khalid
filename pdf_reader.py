# pdf_reader.py

from flask import Blueprint, render_template, request
import fitz  # PyMuPDF library for PDF handling

pdf_reader_app = Blueprint('pdf_reader', __name__)

@pdf_reader_app.route('/project_route', methods=['GET', 'POST'])
def project_route():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        if pdf_file:
            # Read and extract text from the PDF file
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            pdf_text = ""
            for page_num in range(len(pdf_document)):
                pdf_page = pdf_document.load_page(page_num)
                pdf_text += pdf_page.get_text()

            # Optionally, save the extracted text to a file or process it as needed

            return render_template('pdf_reader.html', pdf_text=pdf_text)

    return render_template('pdf_reader.html', pdf_text=None)
