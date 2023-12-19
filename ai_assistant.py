from flask import Blueprint, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

ai_assistant_app = Blueprint('tool1', __name__)

@ai_assistant_app.route('/', methods=['GET', 'POST'])
def project_route():
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # Use OpenAI to generate a response based on user input
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "user", "content": user_input}
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the response text
        ai_response = response

        return render_template('ai_assistant.html', user_input=user_input, ai_response=ai_response)

    return render_template('ai_assistant.html', user_input=None, ai_response=None)
