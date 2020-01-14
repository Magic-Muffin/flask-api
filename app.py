from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///local.db"
# app.config['SQLALCHEMY_BINDS'] = "8080"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/<name>")
def index(name):
    usr = User(username=name)
    db.session.add(usr)
    db.session.commit()
    return '<h1>Added new user</h1>'

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return do_login()
    else:
        return show_register()

def do_login():
    return "POST"

def show_register():
    return "<h1>Register</h1>"

from main import db
db.create_all()