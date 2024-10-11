import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/like', methods=['POST'])
def like_message():
    data = request.get_json()
    message_index = data.get('message_index')

    with open('messages.json', 'r') as f:
        messages = json.load(f)

    if message_index is None or 0< int(message_index) >= len(messages['data']):
        return jsonify({'message': 'Message not found'}), 404

    messages['data'][message_index]['likes'] += 1
    with open('messages.json', 'w') as f:
        json.dump(messages, f)
    return jsonify({'message': 'Message liked successfully', 'likes': messages['data'][message_index]['likes']}), 200

if __name__ == '__main__':
    if not os.path.isfile('messages.json'):
        with open('messages.json', 'w') as f:
            json.dump({'data':{}}, f)
    app.run(port=5003)
