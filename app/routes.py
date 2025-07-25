from flask import (Blueprint, request, jsonify, redirect, url_for,
                   render_template, flash)
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from .models import *
from . import db, bcrypt, login_manager

import random

main = Blueprint("main", __name__)

@main.route('/')
def index():
    return render_template('index.html')

# using the route decorator
@main.route('/check')
@login_required
def health_check():
    return {"message": "pong"}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# USER ROUTES
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = request.form

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        flash('Username and password are required.', 'error')
        return render_template('register.html'), 400

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        flash('Username already exists.', 'error')
        return render_template('register.html'), 400

    # Create user object
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])  # hash password

    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful. You can now log in.',
          'success')
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.form if request.form else request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required.'}), 400

    # get user from db
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        login_user(user)

        # Handle safe redirect after login
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.dashboard')  # default
        return redirect(next_page)

    return jsonify({'error': 'Invalid username or password'}), 401


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# AUV ROUTES/VIEWS

# Get all AUVs
@main.route('/auv', methods=['GET'])
@login_required
def list_all_auvs():
    auvs = AUV.query.all()
    return render_template("auv_list.html", auvs=auvs)


# Create a new AUV
@main.route('/auvs/create', methods=['POST'])
@login_required
def create_auv_html():
    name = request.form.get('name')
    status = request.form.get('status')

    if not name or not status:
        flash("Name and status are required.", 'error')
        return redirect(url_for('main.list_all_auvs'))

    auv = AUV(name=name,
              status=status)

    db.session.add(auv)
    db.session.commit()

    flash("AUV created successfully.", 'success')
    return redirect(url_for('main.list_all_auvs'))


# Read a single AUV by ID
@main.route('/auv/<int:auv_id>', methods=['GET'])
@login_required
def get_auv(auv_id):
    auv = AUV.query.get(auv_id)
    if not auv:
        return jsonify({"error": "AUV not found"}), 404
    return jsonify(auv.to_dict())


# Update an AUV
@main.route('/auvs/edit/<int:auv_id>', methods=['GET'])
@login_required
def edit_auv_form(auv_id):
    auv = AUV.query.get(auv_id)
    if not auv:
        flash("AUV not found.", 'error')
        return redirect(url_for('main.list_auvs'))

    return render_template('edit_auv.html', auv=auv)

@main.route('/auvs/edit/<int:auv_id>', methods=['POST'])
@login_required
def update_auv_html(auv_id):
    print("ID", auv_id)
    auv = AUV.query.get(auv_id)
    print(auv)
    if not auv:
        flash("AUV not found.", 'error')
        return redirect(url_for('main.list_all_auvs'))

    name = request.form.get('name')
    status = request.form.get('status')

    if not name or not status:
        flash("Name and status are required.", 'error')
        return redirect(url_for('main.edit_auv_form', auv_id=auv.id))

    auv.name = name
    auv.status = status
    db.session.commit()

    flash("AUV updated successfully.", 'success')
    return redirect(url_for('main.list_all_auvs'))



# Delete an AUV
@main.route('/auvs/delete/<int:auv_id>', methods=['POST'])
@login_required
def delete_auv_html(auv_id):
    print("XXXXXX++++++XXXXXX", type(auv_id))
    auv = AUV.query.get(auv_id)
    if not auv:
        flash("AUV not found.", 'error')
        return redirect(url_for('main.list_all_auvs'))

    db.session.delete(auv)
    db.session.commit()

    flash("AUV deleted.", 'success')
    return redirect(url_for('main.list_all_auvs'))


# AUV C2
@main.route('/auv/<int:auv_id>/command', methods=['GET', 'POST'])
def command_auv(auv_id):
    auv = AUV.query.get_or_404(auv_id)

    if request.method == 'POST':
        command = request.form.get('command')
        print(f"============{command}============")

        if command == 'start':
            auv.status = 'active'
        elif command == 'stop':
            auv.status = 'idle'
        elif command == 'dive':
            auv.depth = (auv.depth or 0) + 10  # Simulate diving deeper
        elif command == 'surface':
            auv.depth = max((auv.depth or 0) - 10, 0)  # Can't go above surface
        elif command == 'turn_north':
            auv.direction = 'North'
        elif command == 'turn_south':
            auv.direction = 'South'
        elif command == 'simulate':
            auv.temperature = round(2 + 28 * random.random(), 1)
            auv.depth = round(5 + 50 * random.random(), 1)

        db.session.commit()
        flash("Command executed.", "info")
        return redirect(url_for('main.command_auv', auv_id=auv_id))

    return render_template('auv_command.html', auv=auv)
