import requests
import json
import os

# It's better to store your API key as an environment variable
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit()

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
    response.raise_for_status()  # Raise an exception for bad status codes

    response_json = response.json()
    print(json.dumps(response_json, indent=4)) # Pretty print the JSON response

except requests.exceptions.RequestException as e:
    print(f"Error during API call: {e}")
except json.JSONDecodeError:
    print("Error decoding JSON response.")