from flask import request, jsonify, g

def create_task():
    data = request.json
    cursor = g.db.cursor()
    cursor.execute(
        "INSERT INTO tasks (user_id,title,description,priority,due_date) VALUES (%s,%s,%s,%s,%s)",
        (session['user_id'], data['title'], data.get('description'), data['priority'], data['due_date'])
    )
    g.db.commit()
    return jsonify({'status':'ok'})

def get_tasks():
    cursor = g.db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE user_id=%s", (session['user_id'],))
    return jsonify(cursor.fetchall())

# Implement update_task, delete_task similarly