from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

# ================== POSTGRESQL Connection ================== 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/tasksdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ================== Models ==================
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


@app.route("/api/tasks", methods=["POST"])
def submit_task():
    title = request.form.get("title")
    description = request.form.get("description")
    status = request.form.get("status", "todo")
    due_date_str = request.form.get("due_date")

    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

    new_task = Task(
        title=title,
        description=description,
        status=status,
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("tasks_page"))

@app.route("/api/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task_status(task_id):
    task = Task.query.get_or_404(task_id)

    statuses = ["todo", "in_progress", "done"]

    current_index = statuses.index(task.status.lower())
    next_index = (current_index + 1) % len(statuses)
    task.status = statuses[next_index]

    db.session.commit()
    return {"status": task.status}

from flask import request, jsonify

@app.route("/api/tasks", methods=["GET"])
def filter_tasks():
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
    return jsonify([task.to_dict() for task in tasks])


# get single task by task id
@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({ 
            "error": "Task not found", 
            "status": 404
        }), 404

    return jsonify({
        "success": "Task retrieved successfully",
        "status": 200,
        "data": task.to_dict()
    }), 200

# ================== Program Start ================== 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Table Created!")
    app.run(debug=True)