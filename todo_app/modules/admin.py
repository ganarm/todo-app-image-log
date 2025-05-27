from flask import jsonify, g

def get_user_stats():
    cursor = g.db.cursor()
    cursor.execute("SELECT username, COUNT(*) AS tasks FROM users u LEFT JOIN tasks t ON u.id=t.user_id GROUP BY u.id")
    return cursor.fetchall()