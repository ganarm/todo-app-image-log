import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify
from modules.db import get_db
from modules.auth import register_user, authenticate_user, login_required, logout_user, admin_required
from modules.tasks import create_task, get_tasks
from modules.admin import get_user_stats


app = Flask(__name__)

# app.py

db_config = {
    'host':     'localhost',   # your host
    'port':     3307,          # your port (if not 3306)
    'user':     'ganesh',      # your MySQL username
    'password': 'Ganesh',      # your MySQL password
    'database': 'todo_app'     # your database name
}


@app.before_request
def before_request():
    g.db = get_db(db_config)

@app.teardown_request
def teardown_request(exc):
    if hasattr(g, 'db'):
        g.db.close()

# Registration routes
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pattern = request.form['pattern']
        register_user(g.db, username, email, pattern)
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login routes
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pattern = request.form['pattern']
        if authenticate_user(g.db, username, pattern):
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout_route():
    logout_user()
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Todos API
@app.route('/api/tasks', methods=['GET','POST'])
@login_required
def tasks_api():
    if request.method == 'POST':
        return create_task()
    return get_tasks()

# Admin
@app.route('/admin')
@admin_required
def admin_panel():
    stats = get_user_stats()
    return render_template('admin.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)