from flask import request, jsonify

from app import app
from models import User, InputValues, db

# Routes

@app.route('/api/register', methods=['POST'])
def register():
    if not request.json or 'username' not in request.json or 'email' not in request.json or 'password' not in request.json:
        return jsonify({'error': 'Invalid request data'}), 400

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({'error': 'Invalid request data'}), 400

    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/khoj', methods=['POST'])
def khoj():
    if not request.json or 'user_id' not in request.json or 'input_values' not in request.json or 'search_value' not in request.json:
        return jsonify({'error': 'Invalid request data'}), 400

    user_id = request.json['user_id']
    input_values = sorted(map(int, request.json['input_values'].split(',')), reverse=True)
    search_value = int(request.json['search_value'])

    input_values_str = ','.join(map(str, input_values))


    input_data = InputValues(user_id=user_id, input_values=input_values_str)
    db.session.add(input_data)
    db.session.commit()
    search_result = search_value in input_values

    return jsonify({'result': search_result}), 200