from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Define the path to the JSON file
DATA_FILE = 'data.json'

def read_json_data():
    """Reads the data from data.json."""
    if not os.path.exists(DATA_FILE):
        # Return a base structure if the file doesn't exist yet
        return {"data": [], "auth": []}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_json_data(data):
    """Writes the data back to data.json."""
    with open(DATA_FILE, 'w') as f:
        # Use json.dump with indent for readability
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET'])
def root():
    return "Welcome To Chatty. Where You Lick Something Marvelous."

# --- Endpoint 1: /login (POST) ---
@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    username = credentials.get('username')
    email_id = credentials.get('email-id')
    password = credentials.get('password')

    data = read_json_data()
    auth_list = data.get('auth', [])

    # Verify credentials against the auth list
    for user in auth_list:
        if (user.get('username') == username or user.get('email-id') == email_id) and user.get('password') == password:
            return jsonify({"status": "success", "message": "Login successful!"}), 200

    return jsonify({"status": "error", "message": "Invalid credentials."}), 401

# --- Endpoint 2: /send_message (POST) ---
@app.route('/send_message', methods=['POST'])
def send_message():
    message_data = request.get_json()
    # Expects a JSON structure like: {"message": "some text here"}

    if not message_data or 'message' not in message_data:
        return jsonify({"status": "error", "message": "Invalid input format. Expecting {'message': '...'}"}), 400

    data = read_json_data()
    messages_list = data.get('data', [])

    # Generate a new ID (simple approach: max ID + 1, or 0 if list empty)
    new_id = max([item['id'] for item in messages_list], default=-1) + 1
    
    # Get current date in the specified format
    current_date = datetime.now().strftime("%d-%m-%Y")

    new_entry = {
        "id": new_id,
        "date": current_date,
        "data": {"message": message_data['message']}
    }

    messages_list.append(new_entry)
    data['data'] = messages_list # Update the main data dictionary
    write_json_data(data) # Write the entire structure back to the file

    return jsonify({"status": "success", "message": "Message stored successfully", "new_record": new_entry}), 201

# --- Endpoint 3a: /get_messages (GET) ---
@app.route('/get_messages', methods=['GET'])
def get_all_messages():
    data = read_json_data()
    # Return all items in the 'data' list
    return jsonify(data.get('data', [])), 200

# --- Endpoint 3b: /get_messages/<date> (GET) ---
@app.route('/get_messages/<date>', methods=['GET'])
def get_messages_by_date(date):
    # Expected date format is DD-MM-YYYY (e.g., 13-12-2025)
    data = read_json_data()
    messages_list = data.get('data', [])

    # Filter messages where the 'date' field matches the requested date
    filtered_messages = [message for message in messages_list if message.get('date') == date]

    if not filtered_messages:
        return jsonify({"status": "info", "message": f"No messages found for date: {date}"}), 404

    return jsonify(filtered_messages), 200

if __name__ == '__main__':
    # Ensure the data.json file exists with basic structure if running this script directly for the first time
    if not os.path.exists(DATA_FILE):
        write_json_data({"data": [], "auth": []})
        print(f"Created initial {DATA_FILE} file.")
        
    app.run(debug=True)

