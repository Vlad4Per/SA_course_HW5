import os

from flask import Flask, request, jsonify
import json


app = Flask(__name__)


@app.route('/post', methods=['POST'])
def post_message():
    data = request.get_json()
    username = data.get('username')
    text = data.get('text')

    with open('users.json', 'r') as f:
        users = json.load(f)
    with open('messages.json', 'r') as f:
        messages = json.load(f)


    if not username or not text:
        return jsonify({'message': 'Missing username or text'}), 400
    if not username in users:
        return jsonify({'message': 'User not found'}), 400
    if len(text) >= 400:
        return jsonify({'message': 'Message too long'}), 400


    with open('messages.json', 'w') as f:
        messages['data'][len(messages['data'])] = {'username': username, 'text': text, 'likes': 0}
        json.dump(messages, f)

    with open('users.json', 'w') as f:
        users[username]['messages'].append(len(messages['data'])-1)
        json.dump(users, f)

    return jsonify({'message': 'Message posted successfully'}), 201


@app.route('/feed', methods=['GET'])
def get_feed():
    with open('messages.json', 'r') as f:
        messages = json.load(f)
    messages_lst = list(messages['data'].items())
    return jsonify(messages_lst[max(-10, -len(messages['data'])):]), 200


if __name__ == '__main__':
    if not os.path.isfile('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)
    if not os.path.isfile('messages.json'):
        with open('messages.json', 'w') as f:
            json.dump({'data': {}}, f)
    app.run(port=5002)
