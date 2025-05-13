from flask import Flask, request, jsonify, render_template, send_file, url_for, send_from_directory
import csv
import openai
from flask import Response
from flask_cors import CORS
import os, jsonschema_specifications
from dotenv import load_dotenv
import json


from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CSV_PATH = "user_responses.csv"
CORS(app)
# Load model once globally


load_dotenv()  # loads from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")
genai_client = genai.Client(api_key = os.getenv("GEMINI_API_KEY")
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "source files")
USER_STATE_FILE = os.path.join(BASE_DIR, "user_data.json")
USER_LOG_DIR = os.path.join(BASE_DIR, "user_logs")

# Ensure directories and user data storage exist
os.makedirs(USER_LOG_DIR, exist_ok=True)
if not os.path.exists(USER_STATE_FILE):
    with open(USER_STATE_FILE, "w") as f:
        json.dump({}, f)

@app.route("/get_user_data", methods=["POST"])
def get_user_data():
    user_id = request.json["user_id"]
    with open(USER_STATE_FILE) as f:
        state = json.load(f)
    if user_id not in state:
        state[user_id] = {"file": "En-Zh_GPT.csv", "index": 0}
        with open(USER_STATE_FILE, "w") as f:
            json.dump(state, f)
    return jsonify(state[user_id])

@app.route("/get_csv/<filename>")
def get_csv(filename):
    return send_from_directory(DATA_DIR, filename)

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    user_id, index, ranking = data["user_id"], data["index"], data["ranking"]
    log_file = os.path.join(USER_LOG_DIR, f"{user_id}.csv")

    is_new = not os.path.exists(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["index", "ranking"])
        writer.writerow([index, ",".join(ranking)])

    # Update index
    with open(USER_STATE_FILE) as f:
        state = json.load(f)
    state[user_id]["index"] = index + 1
    with open(USER_STATE_FILE, "w") as f:
        json.dump(state, f)

    return {"status": "saved"}

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
