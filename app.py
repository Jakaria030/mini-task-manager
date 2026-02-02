from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import logging
import os


filename = "logs/tasks.log"
folder = os.path.dirname(filename)

# Create logs folder if not exists
if folder:
    os.makedirs(folder, exist_ok=True)

# Logger factory
def get_logger(name="tasks"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

logger = get_logger()

app = Flask(__name__)

# ================== POSTGRESQL Connection ================== 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/tasksdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ================== Model ==================
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False, default='todo')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None
        }
    
# ================== Page Render ================== 
@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/tasks.html", methods=["GET"])
def tasks_page():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

# ================== Router ================== 
# @app.route("/api/tasks", methods=["POST"])
# def submit_task():
#     title = request.form.get("title")
#     description = request.form.get("description")
#     status = request.form.get("status", "todo")
#     due_date_str = request.form.get("due_date")

#     due_date = None
#     if due_date_str:
#         due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

#     new_task = Task(
#         title=title,
#         description=description,
#         status=status,
#         due_date=due_date
#     )

#     db.session.add(new_task)
#     db.session.commit()

#     return redirect(url_for("tasks_page"))

# create task
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    due_date = data.get("due_date")

    if title is None:
        logger.error("Title is not found")
        return jsonify({
            "error": "Title is not found",
            "status": 404
        }), 404
    
    if status and status not in ["todo", "in_progress", "done"]:
        logger.error("Status must be 'todo', 'in_progress', 'done'")
        return jsonify({
            "error": "Status must be 'todo', 'in_progress', 'done'",
            "status": 400
        }), 400

    new_task = Task(
        title=title,
        description=description,
        status=status,
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()
    
    logger.info("Task created successfully")
    return jsonify({
        "success": "Task created successfully",
        "status": 201,
        "data": new_task.to_dict()
    }), 201

# get tasks - all tasks or filter
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    q = request.args.get("q")
    sort = request.args.get("sort")

    query = Task.query

    if status:
        query = query.filter(Task.status == status)
    if q:
        query = query.filter((Task.title.ilike(f"%{q}%")) | (Task.description.ilike(f"%{q}%")))
    if sort in ["due_date","created_at"]:
        query = query.order_by(getattr(Task, sort))

    tasks = query.all()

    logger.info("Task fetched successfully")
    return jsonify({
        "success": "Tasks fetched successfully",
        "status": 200,
        "data": [task.to_dict() for task in tasks]
    }), 200

# toggle status cyclic order
@app.route("/api/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task_status(task_id):
    task = Task.query.get_or_404(task_id)

    statuses = ["todo", "in_progress", "done"]

    current_index = statuses.index(task.status.lower())
    next_index = (current_index + 1) % len(statuses)
    task.status = statuses[next_index]

    db.session.commit()

    logger.info("Toggle status successfully")
    return jsonify({
        "success": "Toggle status successfully",
        "status-code": 200,
        "status": task.status
    }), 200

# get single task by task id
@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        logger.error(f"Task not found for id: {task_id}")
        return jsonify({ 
            "error": f"Task not found for id: {task_id}", 
            "status": 404
        }), 404

    logger.info("Task fetched successfully")
    return jsonify({
        "success": "Task fetched successfully",
        "status": 200,
        "data": task.to_dict()
    }), 200

# update task
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        logger.error(f"Task not found {task_id}")
        return jsonify({
            "error": f"Task not found {task_id}",
            "status": 404
        }), 404

    data = request.get_json()
    if not data:
        logger.error("No data provided")
        return jsonify({
            "error": "No data provided",
            "status": 400
        }), 400

    if data.get("status", None) and data.get("status") not in ["todo", "in_progress", "done"]:
        logger.error("Status must be 'todo', 'in_progress', 'done'")
        return jsonify({
            "error": "Status must be 'todo', 'in_progress', 'done'",
            "status": 400
        }), 400
    
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    task.due_date = data.get("due_date", task.due_date)

    db.session.commit()

    logger.info("Task updated successfully")
    return jsonify({
        "success": "Task updated successfully",
        "status": 200,
        "data": task.to_dict()
    }), 200

# delete task by id
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        logger.error(f"Task not found for id: {task_id}")
        return jsonify({
            "error": f"Task not found for id: {task_id}",
            "status": 404
        }), 404

    db.session.delete(task)
    db.session.commit()

    logger.info("Task deleted successfully")
    return jsonify({
        "success": "Task deleted successfully",
        "status": 200
    }), 200

# ================== Program Start ================== 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Table Created!")
    app.run(debug=True)