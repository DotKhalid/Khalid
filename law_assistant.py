from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from datetime import datetime
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.Client(api_key=api_key)



# Function to handle the chat with the assistant
def assistant_chatbot(user_query, thread_id=None, file_id=None):
    if thread_id is None:
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread_id = thread_id

    if file_id:
        # Create a message with the file attachment
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_query,
            file_ids=[file_id]  # Attach the file by its ID
        )
        print("File ID sent to assistant:", file_id)  # Print the file ID
    else:
        # If no file ID is provided, create a message without an attachment
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_query
        )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id="asst_u1Y4r1YhBOwVxhNJsNa2NLoG",
        instructions="Provide information related to law queries according to Pakistani law. Remember, if you don't know the answer, please don't hallucinate; refer to law professionals.",
    )

    # Wait for the run to complete
    while not run.completed_at:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    last_message = messages.data[0]
    response = last_message.content[0].text.value

    return response, thread_id



law_assistant_app = Blueprint('law_assistant', __name__)

# Initialize 'messages' in the session using before_request
@law_assistant_app.before_request
def before_request():
    if 'messages' not in session:
        session['messages'] = []

@law_assistant_app.route('/')
def home():
    return render_template('law_assistant.html')

from werkzeug.utils import secure_filename

@law_assistant_app.route('/law_assistant', methods=['POST'])
def chat():
    user_query = request.form['query']
    user_file = request.files['file']
    print(user_file)
    print(user_query)
    if user_query.strip():
        response, thread_id = assistant_chatbot(user_query, session.get('thread_id'))
        session['thread_id'] = thread_id
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session['messages'].append((timestamp, user_query))
        session['messages'].append((timestamp, response))

    if user_file:
        print("Uploaded file type:", user_file.content_type)
        # Ensure a secure filename to prevent any potential security issues
        filename = secure_filename(user_file.filename)

        # Save the uploaded file locally (you can adjust the path as needed)
        file_path = os.path.join('static', 'uploads', filename)
        user_file.save(file_path)

        # Now, you can upload the saved file to OpenAI
        with open(file_path, 'rb') as file_data:
            file = client.files.create(
                file=file_data,
                purpose='assistants'
            )
        
        file_id = file.id
        
        print("File ID coming from chat:", file_id)
        response, thread_id = assistant_chatbot(user_query, session.get('thread_id'), file_id)
        session['thread_id'] = thread_id
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session['messages'].append((timestamp, user_query))
        session['messages'].append((timestamp, response))
    
    return redirect(url_for('law_assistant.home'))


@law_assistant_app.route('/clear', methods=['POST'])
def clear_chat():
    thread_id = session.get('thread_id')

    if thread_id:
        # Delete the thread if a thread ID is available
        client.beta.threads.delete(thread_id)

    # Clear the session messages
    session['messages'] = []

    # Redirect to the '/law_assistant/' URL
    return redirect(url_for('law_assistant'))


