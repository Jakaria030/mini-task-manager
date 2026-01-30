from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks.html")
def tasks():
    return render_template("tasks.html")