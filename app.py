from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

# ================== POSTGRESQL Connection ================== 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/taskdb'
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
    return render_template('tasks.html')

@app.route("/api/tasks", methods=["POST"])
def submit_task():
    title = request.form.get("title")
    description = request.form.get("description")
    status = request.form.get("status")
    due_date = request.form.get("due_date")

    print(title, description, status, due_date)

    return redirect(url_for("tasks_page"))


# ================== Program Start ================== 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)