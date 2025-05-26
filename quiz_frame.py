from flask import Flask, send_file, request, jsonify
import json
import os

app = Flask(__name__, static_folder='public')

# JSON file to store answers
data_file = 'answers.json'
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump({"users": {}}, f)

daily_question = {
    "id": "2025-05-25",
    "text": "When was Warpcast rebranded?",
    "options": ["A", "B"],
    "correct": "A"
}

@app.route('/')
def welcome():
    return send_file('public/index.html')

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    fid = data.get('untrustedData', {}).get('inputText', 'unknown')
    button_index = data.get('untrustedData', {}).get('buttonIndex', 0)

    selected_option = daily_question["options"][button_index - 1] if button_index <= 2 else None
    if not selected_option:
        return jsonify({"message": "Invalid answer"}), 400

    with open(data_file, 'r') as f:
        users = json.load(f)

    if fid not in users["users"]:
        users["users"][fid] = {"points": 0}

    is_correct = selected_option == daily_question["correct"]
    users["users"][fid]["points"] += 50 if is_correct else 0

    with open(data_file, 'w') as f:
        json.dump(users, f)

    return jsonify({"message": f"{'Correct' if is_correct else 'Wrong'}! Points: {users['users'][fid]['points']}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
