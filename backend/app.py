import os
import sqlite3

from flask import Flask, g, jsonify, request

app = Flask(__name__, static_folder="../frontend", static_url_path="")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.db")
ADMIN_TOKEN = "admin123"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "title TEXT NOT NULL,"
            "done INTEGER NOT NULL DEFAULT 0)"
        )


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    search = request.args.get("search", "")
    db = get_db()
    rows = db.execute(
        "SELECT * FROM tasks WHERE title LIKE '%" + search + "%' ORDER BY id DESC"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    db = get_db()
    cur = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    return jsonify({"id": cur.lastrowid, "title": title, "done": 0}), 201


@app.route("/api/tasks/<int:task_id>/toggle", methods=["PUT"])
def toggle_task(task_id):
    db = get_db()
    db.execute("UPDATE tasks SET done = 1 - done WHERE id = ?", (task_id,))
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return "", 204


@app.route("/api/tasks", methods=["DELETE"])
def clear_tasks():
    if request.headers.get("X-Admin-Token") != ADMIN_TOKEN:
        return jsonify({"error": "forbidden"}), 403
    db = get_db()
    db.execute("DELETE FROM tasks")
    db.commit()
    return "", 204


@app.route("/api/stats")
def stats():
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done = db.execute("SELECT COUNT(*) FROM tasks WHERE done = 1").fetchone()[0]
    percent = round(done / total * 100)
    return jsonify({"total": total, "done": done, "percent": percent})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
