# app.py

from flask import Flask, render_template
from finance_gpt import finance_gpt_app
from quiz_generator import quiz_app
from law_assistant import law_assistant_app

app = Flask(__name__)
app.secret_key = '123456789'


# Define routes for different projectsss
@app.route('/')
def home():
    return render_template('index.html')

# Register the project-specific apps
app.register_blueprint(finance_gpt_app, url_prefix='/finance_gpt')
app.register_blueprint(quiz_app, url_prefix='/quiz_generator')
app.register_blueprint(law_assistant_app, url_prefix='/law_assistant')

if __name__ == '__main__':
    app.run(port=8000,debug=True)
