import uuid
import re
import collections
from flask import Flask
from flask import render_template
from flask import request
#from flask import SQLAlchemy

app = Flask(__name__)
users_data = [{"name": "test", "age": 20, "hobby": ["test1", "test2"]},
              {"name": "glebas", "age": 18, "hobby": ["sfdgsdg", "sdfg"]}]

dialogs = collections.defaultdict(list)

@app.route('/users', methods=['POST'])
def create_new_user():
    info = request.json
    new_id = {"user_id": str(uuid.uuid4())}
    new_user_data = {**info, **new_id}
    users_data.append(new_user_data)
    print(new_user_data)
    print(users_data)
    return new_id

@app.route('/users', methods=['GET'])
def find_a_users():
    search_results = list(filter(lambda user: request.args.get('q') in user["name"], users_data))
    return search_results

@app.route('/messages/<conversation_id>', methods=['POST'])
def post_new_messages(conversation_id):
    request_body = request.json
    sender = request_body["sender"]
    message_text = request_body["message"]
    message_id = str(uuid.uuid4())
    dialog_id = sorted(conversation_id.split('_'))
    if (dialogs.get( f'{dialog_id[0]}_{dialog_id[1]}') or dialogs.get(f'{dialog_id[1]}_{dialog_id[0]}')) or KeyError:
        dialogs[f'{dialog_id[0]}_{dialog_id[1]}'].append({'text': message_text , 'sender': sender, 'message_id': message_id})
    print(dialogs)
    return message_id

@app.route('/messages/<conversation_id>', methods=['GET'])
def get_dialogs(conversation_id):
    dialog_id = sorted(conversation_id.split('_'))
    result_of_search = dialogs.get(f'{dialog_id[0]}_{dialog_id[1]}')
    if result_of_search == None:
        result_of_search = dialogs.get(f'{dialog_id[1]}_{dialog_id[0]}')
    return result_of_search

@app.route('/messages/<conversation_id>/<message_id>' , methods = ['PATCH'])
def edit_message(conversation_id, message_id):
    new_text = request.json['text']
    dialog = dialogs.get(conversation_id)
    for message in dialog:
        if message['message_id'] == message_id:
            message['text'] = new_text
    return dialogs[conversation_id]


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    return f'Hello, {name}'


@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
