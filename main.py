import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_NAME = "todo.db"

def init_db():
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS tasks (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
			completed INTEGER DEFAULT 0)
	""")

	conn.commit()
	conn.close()

@app.before_request
def log_request_payload():
    if request.method in ["POST", "PUT"]:
        data = request.get_json(silent=True)

        print(f"[{request.method}] Маршрут: {request.path} | Данные: {data}", flush=True)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/tasks", methods = ["GET"])
def get_tasks():
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()

	cursor.execute("SELECT id, title, completed FROM tasks")
	rows = cursor.fetchall()

	conn.close()

	tasks = []
	for row in rows:
		tasks.append(
			{
				"id": row[0],
				"title": row[1],
				"completed": bool(row[2]),
			}
		)

	return jsonify(tasks)

@app.route("/api/tasks", methods = ["POST"])
def add_task():
	data = request.json
	task_title = data.get("title")

	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()

	cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task_title,))
	conn.commit()

	task_id = cursor.lastrowid
	conn.close()

	return jsonify({"id": task_id, "title": task_title, "completed": False})

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json

    completed = 1 if data.get("completed") else 0

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()

    return jsonify({"success": True})


if __name__ == "__main__":
	init_db()
	app.run(debug = True, host = "0.0.0.0", port = 1024)
