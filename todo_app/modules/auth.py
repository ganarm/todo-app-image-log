import os
from flask import request, redirect, url_for, flash, session, g
from modules.utils import hash_pattern, record_login
from modules.db import get_db
from functools import wraps
import bcrypt

SALT = os.getenv('HASH_SALT', '')

def register_user(db, username, email, pattern_raw):
    pattern_hash = hash_pattern(pattern_raw, SALT)
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, image_pattern_hash) VALUES (%s,%s,%s)",
        (username, email, pattern_hash)
    )
    db.commit()

def authenticate_user(db, username, pattern_raw):
    pattern_hash = hash_pattern(pattern_raw, SALT)
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, image_pattern_hash FROM users WHERE username=%s", (username,)
    )
    user = cursor.fetchone()
    if user and user['image_pattern_hash'] == pattern_hash:
        record_login(db, user['id'], True)
        session['user_id'] = user['id']
        return True
    if user:
        record_login(db, user['id'], False)
    return False

# Decorators
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def logout_user():
    session.clear()

# Admin check (example: user_id==1)
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_id') != 1:
            flash('Admin access only.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated