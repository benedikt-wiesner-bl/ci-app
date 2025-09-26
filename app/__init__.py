import os
import sqlite3
from flask import Flask, jsonify, request, render_template, redirect, url_for


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(os.path.dirname(BASE_DIR), "data", "todos.db")
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
# os.makedirs("data", exist_ok=True)
# DB_FILE = "data/todos.db"


def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT 0
                )""")
    conn.commit()
    conn.close()


init_db()


def fetch_todos():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, task, done FROM todos")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "task": r[1], "done": bool(r[2])} for r in rows]


@app.route("/")
def home():
    return render_template("index.html", todos=fetch_todos())


@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task")
    if task:
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO todos (task, done) VALUES (?, 0)", (task,))
        conn.commit()
        conn.close()
    return redirect(url_for("home"))


@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT done FROM todos WHERE id=?", (todo_id,))
    row = c.fetchone()
    if row:
        new_done = 0 if row[0] else 1
        c.execute("UPDATE todos SET done=? WHERE id=?", (new_done, todo_id))
        conn.commit()
    conn.close()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(fetch_todos())


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, task, done FROM todos WHERE id=?", (todo_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return jsonify(error="Not Found"), 404
    return jsonify({"id": row[0], "task": row[1], "done": bool(row[2])})


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify(error="Task field required"), 400
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO todos (task, done) VALUES (?, 0)", (data["task"],))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id, "task": data["task"], "done": False}), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, task, done FROM todos WHERE id=?", (todo_id,))
    row = c.fetchone()
    if row is None:
        conn.close()
        return jsonify(error="Not Found"), 404
    new_task = data.get("task", row[1])
    new_done = int(data.get("done", row[2]))
    c.execute("UPDATE todos SET task=?, done=? WHERE id=?", (new_task, new_done, todo_id))
    conn.commit()
    conn.close()
    return jsonify({"id": todo_id, "task": new_task, "done": bool(new_done)})


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo_api(todo_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
    return jsonify(message="Deleted"), 200



@app.route("/health")
def health():
    return {"status": "ok"}, 200

