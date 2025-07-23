from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from .models import *
from . import db, bcrypt, login_manager


main = Blueprint("routes", __name__)


# Associate the url route "/" with health_check() view function
# using the route decorator
@main.route("/")
def health_check():
    return {"message": "pong"}


# ✅ Create a new AUV
@main.route('/auv', methods=["POST"])
def create_auv():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('status'):
        return jsonify({"error": "Missing 'name' or 'status'"}), 400

    new_auv = AUV(name=data['name'], status=data['status'])
    db.session.add(new_auv)
    db.session.commit()

    return jsonify(new_auv.to_dict()), 201


# ✅ Read a single AUV by ID
@main.route('/auv/<int:auv_id>', methods=['GET'])
def get_auv(auv_id):
    auv = AUV.query.get(auv_id)
    if not auv:
        return jsonify({"error": "AUV not found"}), 404
    return jsonify(auv.to_dict())


# ✅ Update an AUV
@main.route('/auv/<int:auv_id>', methods=['PUT'])
def update_auv(auv_id):
    auv = AUV.query.get(auv_id)
    if not auv:
        return jsonify({"error": "AUV not found"}), 404

    data = request.get_json()
    if 'name' in data:
        auv.name = data['name']
    if 'status' in data:
        auv.status = data['status']

    db.session.commit()
    return jsonify(auv.to_dict())


# ✅ Delete an AUV
@main.route('/auv/<int:auv_id>', methods=['DELETE'])
def delete_auv(auv_id):
    auv = AUV.query.get(auv_id)
    if not auv:
        return jsonify({"error": "AUV not found"}), 404

    db.session.delete(auv)
    db.session.commit()
    return jsonify({"message": "AUV deleted"})


# ✅ Get all AUVs
@main.route('/auv', methods=['GET'])
def get_all_auvs():
    auvs = AUV.query.all()
    return jsonify([auv.to_dict() for auv in auvs])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required.'}), 400

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists.'}), 400

    # Create user object
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])  # hash password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201

@main.route('/login', methods=['POST'])
def login():
    print("Logging in")
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required.'}), 400

    # get user from db
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


