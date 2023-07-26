from flask import Flask, request, jsonify, g  
from datetime datetime  
import sqlite3  
  
app = Flask(__name__)  
  
# Configuration  
DATABASE = 'ami_coding_pari_na.db'  
SECRET_KEY = 'VG5hEGM9L7qIEeYC' # Change this to a strong secret key  
  
# Database Helper Functions  
  
def get_db():  
    db = getattr(g, '_database', None)  
    if db is None:  
        db = g._database = sqlite3.connect(DATABASE)  
        db.row_factory = sqlite3.Row  
    return db  
  
@app.teardown_appcontext  
def close_connection(exception):  
    db = getattr(g, '_database', None)  
    if db is not None:  
        db.close()  
  
def create_tables():  
    db = get_db()  
    with app.open_resource('schema.sql', mode='r') as f:  
        db.cursor().executescript(f.read())  
    db.commit()  
  
def insert_input_values(user_id, input_values):  
    db = get_db()  
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    db.execute('INSERT INTO input_values (user_id, input_values, timestamp) VALUES (?, ?, ?)',  
               (user_id, input_values, timestamp))  
    db.commit()  
  
def get_input_values_by_user_id(user_id, start_datetime, end_datetime):  
    db = get_db()  
    query = 'SELECT timestamp, input_values FROM input_values WHERE user_id=? AND timestamp BETWEEN ? AND ?'  
    result = db.execute(query, (user_id, start_datetime, end_datetime)).fetchall()  
    return [{'timestamp': row['timestamp'], 'input_values': row['input_values']} for row in result]  
  
def create_user(username, password):  
    db = get_db()  
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))  
    db.commit()  
  
def get_user_by_username(username):  
    db = get_db()  
    query = 'SELECT * FROM users WHERE username=?'  
    result = db.execute(query, (username,)).fetchone()  
    if result is None:  
        return None  
    else:  
        return {'id': result['id'], 'username': result['username'], 'password': result['password']}  
  
def authenticate(username, password):  
    user = get_user_by_username(username)  
    if user is not None and user['password'] == password:  
        return user  
    else:  
        return None  
  
# Routes  
  
@app.route('/api/register', methods=['POST'])  
def register():  
    if not request.json or 'username' not in request.json or 'password' not in request.json:  
        return jsonify({'error': 'Invalid request data'}), 400  
  
    username = request.json['username']  
    password = request.json['password']  
  
    # Check if the username already exists  
    if get_user_by_username(username) is not None:  
        return jsonify({'error': 'Username already exists'}), 400  
  
    # Create a new user  
    create_user(username, password)  
  
    return jsonify({'status': 'success', 'message': 'User created successfully'}), 201  
  
@app.route('/api/login', methods=['POST'])  
def login():  
    if not request.json or 'username' not in request.json or 'password' not in request.json:  
        return jsonify({'error': 'Invalid request data'}), 400  
  
    username = request.json['username']  
    password = request.json['password']  
  
    # Authenticate the user  
    user = authenticate(username, password)  
  
    if user is None:  
        return jsonify({'error': 'Invalid username or password'}), 401  
    else:  
        return jsonify({'status': 'success', 'message': 'User authenticated successfully', 'user_id': user['id']}), 200  
  
