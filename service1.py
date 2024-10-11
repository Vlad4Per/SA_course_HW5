import os.path

from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')

    with open('users.json', 'r') as f:
        users = json.load(f)

    if username in users:
        print(username, users)
        return jsonify({'message': 'User already exists'}), 400

    users[username] = {'messages': []}

    with open('users.json', 'w') as f:
        json.dump(users, f, ensure_ascii=False)
    return jsonify({'message': 'User registered successfully'}), 201


if __name__ == '__main__':
    if not os.path.isfile('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)
    app.run(port=5001)
