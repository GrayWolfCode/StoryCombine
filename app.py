from flask import Flask, request, jsonify
from flask_cors import CORS  # <- Add this import
import openai
import json
import io
import os
app = Flask(__name__)
CORS(app)  # <- Add this to enable CORS for all routes

# Ideally, store this securely using environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


@app.route('/combine', methods=['POST'])
def combine_text():
    data = request.json
    combined_text = data['editor1'] + data['editor2'] + \
        data['editor3'] + "Complete this story"
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": combined_text}
            ]
        )
        txt = response.choices[0].message['content']
        text_without_quotes = txt.replace('"', "'")

        return jsonify({'message': text_without_quotes})

    except Exception as e:
        return jsonify({'message': 'Error occurred. Please try again.'}), 500
