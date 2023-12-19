# app.py

from flask import Flask, render_template
from pdf_reader import pdf_reader_app
from ai_assistant import ai_assistant_app
from finance_gpt import finance_gpt_app

app = Flask(__name__)

# Define routes for different projectsss
@app.route('/')
def home():
    return render_template('index.html')

# Register the project-specific apps
app.register_blueprint(pdf_reader_app, url_prefix='/pdf_reader')
app.register_blueprint(finance_gpt_app, url_prefix='/finance_gpt')

if __name__ == '__main__':
    app.run(port=8000,debug=True)
