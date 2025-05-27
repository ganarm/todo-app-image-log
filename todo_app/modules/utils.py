import hashlib, os
from flask import session

def hash_pattern(pattern: str, salt: str):
    return hashlib.sha256((pattern + salt).encode()).hexdigest()

def record_login(db, user_id, success: bool):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO login_attempts (user_id, success) VALUES (%s, %s)",
        (user_id, success)
    )
    db.commit()

def prevent_sql_injection(val):
    # Using parameterized queries elsewhere prevents injection
    return val