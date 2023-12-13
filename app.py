# app.py

from flask import Flask, render_template
from pdf_reader import pdf_reader_app
from ai_assistant import ai_assistant_app

# from image_generation import project_app as image_generation_app  # Import the image generation app

app = Flask(__name__)

# Define routes for different projects
@app.route('/')
def home():
    return render_template('index.html')

# Register the project-specific apps
app.register_blueprint(pdf_reader_app, url_prefix='/pdf_reader')
app.register_blueprint(ai_assistant_app, url_prefix='/ai_assistant')
# app.register_blueprint(image_generation_app, url_prefix='/image_generation')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)
