from flask import Flask, jsonify, request
from backend.langgraph_agent import MasterAgent
from flask_cors import CORS
import logging
logging.basicConfig(level=logging.DEBUG)

backend_app = Flask(__name__)

@backend_app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Running"}), 200

@backend_app.route('/generate_recipebook', methods=['POST'])
def generate_recipebook():
    logging.debug(f"Received data: {request.json}")

    data = request.json
    master_agent = MasterAgent()
    recipebook = master_agent.run(data["keywords"], data["layout"])

    logging.debug(f"Generated recipebook path: {recipebook}")

    return jsonify({"path": recipebook}), 200

