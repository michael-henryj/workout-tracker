from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from storage import save_user, get_user_by_username

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Basic validation
    if not username or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    # Check if user already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        return jsonify({'message': 'Username already in use. Please try again'}), 409

    # Hash the password and save
    password_hash = generate_password_hash(password)
    save_user(username, email, password_hash)

    return jsonify({'message': f'''Account created successfully.
                                    Welcome {username}!'''}), 201

@auth.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'All fields are required'}), 400

    user = get_user_by_username(username)

    # Check user exists and password is correct
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    login_user(user)
    return jsonify({'message': f'Welcome back {username}!'})

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200