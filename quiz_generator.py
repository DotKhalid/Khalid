from flask import Flask,Blueprint, render_template, request, jsonify
from openai import OpenAI

quiz_app = Blueprint('quiz_generator', __name__)

api_key = "hello world"

client = OpenAI(api_key=api_key)

@quiz_app.route('/', methods=['GET', 'POST'])
def generate_quiz():
    questions = None  # Initialize to None

    if request.method == 'POST':
        topic = request.form['topic']
        level = request.form['level']
        num_questions = int(request.form['num_questions'])
        
        # Generate quiz questions using OpenAI's GPT-4
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Generate {num_questions} MCQs about {topic} at {level} level."},
                {"role": "user", "content": ""}
            ]
        )
        questions = response.choices[0].message.content

    return render_template('quiz_generator.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
