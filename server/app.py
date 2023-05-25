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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = Message.query.order_by('created_at').all()

    if request.method == 'GET':
        message_dict = [message.to_dict() for message in messages]
        response = make_response(
            message_dict,
            200
        )
        return response
    
    elif request.method == 'POST':
        new_message = Message(
            body=request.json.get('body'),
            username=request.json.get('username'),
        )
        print(request.json.get('body'))
        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()
        print(message_dict)
        response = make_response(
            message_dict,
            201
        )
        return response

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        for key in request.json:
                setattr(message, key, request.json.get(key))
        
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
             message_dict,
             200
        )
        return response
    
    elif request.method == 'DELETE':
         db.session.delete(message)
         db.session.commit()

         response = make_response(
              "",
              200
         )
         return response

if __name__ == '__main__':
    app.run(port=5555)
