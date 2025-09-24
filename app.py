from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

todos = [
    {"id": 1, "task": "Task 1", "done": False},
    {"id": 2, "task": "Task 2", "done": True}
]

@app.route("/")
def home():
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task")
    if task:
        new_id = max(t["id"] for t in todos) + 1 if todos else 1
        todos.append({"id": new_id, "task": task, "done": False})
    return redirect(url_for("home"))

@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo:
        todo["done"] = not todo["done"]
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return redirect(url_for("home"))


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify(error="Not Found"), 404
    return jsonify(todo)

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify(error="Task field required"), 400
    new_id = max(t["id"] for t in todos) + 1 if todos else 1
    todo = {"id": new_id, "task": data["task"], "done": False}
    todos.append(todo)
    return jsonify(todo), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify(error="Not Found"), 404
    data = request.get_json()
    todo["task"] = data.get("task", todo["task"])
    todo["done"] = data.get("done", todo["done"])
    return jsonify(todo)

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo_api(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify(message="Deleted"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
