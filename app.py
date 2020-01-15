from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///local.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, location='json')
parser.add_argument('password', type=str, location='json')

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.now())
    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/add/<name>")
def index(name):
    usr = UserModel(username=name, password=generate_password_hash("test"))
    db.session.add(usr)
    db.session.commit()
    return f'<h1>Added new user {name}</h1>'

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return do_login()
    else:
        return show_register()

def do_login():
    args = parser.parse_args()
    username = args['username']
    password = args['password']
    if username == None:
        return jsonify({"error": f"Missing username argument."}, 400 )
    if password == None:
        return jsonify({"error": f"Missing password argument."}, 400 )
    user = db.session.query(UserModel).filter_by(username=username).first()
    if user == None:
        return jsonify({"error": f"Could not find user {username}."}, 400 )
    if check_password_hash(user.password, password):
        return jsonify({"success": "Login success"})
    return jsonify({"error": "Incorrect password"})
    
def show_register():
    
    return "<h1>Register</h1>"

class UserList(Resource):
    def get(self):
        users = db.session.query(UserModel).all()
        ret = {}
        for user in users:
            ret[user.id] = {"username": user.username, "password": user.password, "date_created": str(user.date_created)}
        return ret

class User(Resource):
    def get(self, user_id):
        user = db.session.query(UserModel).filter_by(id=user_id).first()
        if user != None:
            return {user.id :{
                    "username": user.username, 
                    "password": user.password, 
                    "date_created": str(user.date_created)}
                }
        return {"error": f"User not found by id {user_id}"}, 404

class CreateUser(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        if username == None:
            return {"error": f"Missing username argument."}, 400 
        if password == None:
            return {"error": f"Missing password argument."}, 400 
        test = db.session.query(UserModel).filter_by(username=username).first()
        if test != None:
            return {"error": f"Username {username} already exists."}, 400 
        hashed_password = generate_password_hash(password)
        user = UserModel(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return {"success": f"user {username} created"}, 201

api.add_resource(UserList, '/users')
api.add_resource(CreateUser, '/adduser')
api.add_resource(User, '/user/<user_id>')

if __name__ == "__main__":
    from app import db
    db.create_all()
    app.run(debug=True)