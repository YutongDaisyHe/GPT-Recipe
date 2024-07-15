from flask import Flask, jsonify, request
from backend.langgraph_agent import MasterAgent
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask application
backend_app = Flask(__name__)
CORS(backend_app)  # Enable Cross-Origin Resource Sharing (CORS)

@backend_app.route('/', methods=['GET'])
def index():
    """
    Root endpoint to check the status of the application.

    Returns
    -------
    Response
        A JSON response with the status of the application.
    """
    return jsonify({"status": "Running"}), 200

@backend_app.route('/generate_recipebook', methods=['POST'])
def generate_recipebook():
    """
    Endpoint to generate a recipe book based on provided keywords and layout.

    Receives JSON data with 'keywords' and 'layout', processes them using the MasterAgent,
    and returns the path to the generated recipe book.

    Returns
    -------
    Response
        A JSON response with the path to the generated recipe book.
    """
    logging.debug(f"Received data: {request.json}")

    data = request.json
    master_agent = MasterAgent()
    recipebook = master_agent.run(data["keywords"], data["layout"])

    logging.debug(f"Generated recipebook path: {recipebook}")

    return jsonify({"path": recipebook}), 200

# Run the Flask application
if __name__ == '__main__':
    backend_app.run(debug=True)
