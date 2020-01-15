from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///local.db"
# app.config['SQLALCHEMY_BINDS'] = "8080"
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/add/<name>")
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

class HelloWorld(Resource):
    def get(self):
        users = db.session.query(User).all()
        ret = {}
        for user in users:
            ret[user.id] = {"username": user.username, "date_created": str(user.date_created)}
        return ret

api.add_resource(HelloWorld, '/')

if __name__ == "__main__":
    from app import db
    db.create_all()
    app.run(debug=True)