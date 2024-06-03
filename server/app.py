from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.order_by(Message.created_at).all() #List of objects
        serialized_messages = [message.to_dict() for message in all_messages] #List of dictionaries
        return make_response(serialized_messages, 200)
    elif request.method == 'POST':
        request_dict = request.get_json()
        new_message = Message(username = request_dict['username'], body = request_dict['body'])

        db.session.add(new_message)
        db.session.commit()
 
        added_message = new_message.to_dict()
        return make_response(added_message, 201)

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()

    if message:
        if request.method == 'PATCH':
            edited_message = request.get_json()
            message.body = edited_message['body']

            db.session.add(message)
            db.session.commit()

            message_dict = message.to_dict()
            return make_response(message_dict, 200)
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response = {
                'message': f'Message {id} deleted.'
            }

            return make_response(response, 200)
        return ''
    else:
        response = {
            'message': f'Message {id} not found.'
        }

        return make_response(response, 404)

if __name__ == '__main__':
    app.run(port=5555)
