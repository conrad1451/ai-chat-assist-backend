from flask import Flask, jsonify, request
from flask_cors import CORS

import requests
import json
import os
import logging # Import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_key = os.environ.get("GEMINI_PERSONAL_API_KEY")

if not api_key:
    logging.error("Error: GEMINI_PERSONAL_API_KEY environment variable not set at app startup.")

@app.route('/')
def hello_world():
    return 'Conrad deployed his first Flask App! He just wants to say one thing ... Hello, World!'

@app.route('/explain_ai')
def explain_ai():
    if not api_key:
        logging.error("API key missing in /explain_ai request.")
        return jsonify({"error": "GEMINI_PERSONAL_API_KEY environment variable not set."}), 500 # Return 500 if key is genuinely missing

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [{"text": "Explain how AI works"}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        response_json = response.json()
        return jsonify(response_json)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API call to Gemini in /explain_ai: {e}")
        return jsonify({"error": f"Error during API call: {e}"}), 500
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON response from Gemini in /explain_ai. Response content: {response.text}")
        return jsonify({"error": "Error decoding JSON response from Gemini."}), 500

@app.route('/gemini-chat')
def gemini_chat():
    if not api_key:
        logging.error("API key missing in /gemini-chat request.")
        return jsonify({"error": "GEMINI_PERSONAL_API_KEY environment variable not set."}), 500

    user_input = request.args.get('text')
    logging.info(f"Received user_input: '{user_input}'") # Log the received input

    if not user_input:
        logging.warning("Missing 'text' parameter in /gemini-chat query string.")
        return jsonify({"error": "Missing 'text' parameter in the query string."}), 400 # Bad Request if no text

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [{"text": user_input}]
            }
        ]
    }
    logging.info(f"Sending data to Gemini: {json.dumps(data)}") # Log the payload

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        logging.info("Gemini API call successful for /gemini-chat.")
        return jsonify(response_json)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API call to Gemini in /gemini-chat: {e}. Response status: {response.status_code}, content: {response.text}")
        return jsonify({"error": f"Error during API call: {e}"}), 500
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON response from Gemini in /gemini-chat. Response content: {response.text}")
        return jsonify({"error": "Error decoding JSON response."}), 500
    
if __name__ == '__main__':
    app.run(debug=True)