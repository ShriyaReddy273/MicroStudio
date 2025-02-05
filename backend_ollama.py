import logging
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(_name_)

app = Flask(_name_)
CORS(app)  # Allow frontend requests

# Ollama local API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        logger.warning("No input provided in request.")
        return jsonify({"error": "No input provided"}), 400

    logger.info(f"Received request: {user_input}")

    payload = {
        "model": "llama2",  # Change this if using a different model
        "prompt": user_input,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response_data = response.json()
        logger.info(f"Response from Ollama: {response_data}")
        return jsonify({"response": response_data.get("response", "No response")})
    except Exception as e:
        logger.error(f"Error communicating with Ollama: {str(e)}")
        return jsonify({"error": str(e)})

if _name_ == '_main_':
    logger.info("Starting Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
