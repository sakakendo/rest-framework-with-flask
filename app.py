from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_migrate import Migrate
from abc import ABCMeta

from models import User, Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140), nullable=False)
    state = db.Column(db.Integer, nullable=False)

class APIBaseError(Exception):
    status_code = None
    code = None
    message = ""

    def __init__(self, message):
        self.message = message

    def json(self):
        return {
            "error": {
                "code": self.code,
                "message": self.message
            }
        }

class NotFound(APIBaseError):
    status_code = 404
    code = "NotFound"

class InvalidParamField(APIBaseError):
    status_code = 421
    code = "InvalidParamField"

class Serializer():
    class Meta:
        model = None
        fields = []

    @classmethod
    def get_all(cls):
        res = []
        for obj in cls.Meta.model.query.all():
            res.append({
                field : obj.__dict__.get(field) for field in cls.Meta.fields
            })
        return res

    @classmethod
    def get_one(cls, _id):
        obj = cls.Meta.model.query.filter_by(id=_id).first()
        if obj is None:
            raise NotFound(f'cannot found : {_id}')
        res={ field : obj.__dict__.get(field) for field in cls.Meta.fields}
        return res

    @classmethod
    def create(cls, param):
        print(param)
        for key in param.keys():
            if key not in cls.Meta.fields: 
                raise InvalidParamField(f'param field {key} is invalid')
        try: 
            model = cls.Meta.model(**param)
            db.session.add(model)
            db.session.commit()
            return str(model)
        except exc.IntegrityError as e:
            raise InvalidParamField(f'failed to insert new model')

class UserSerializer(Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TodoSerializer(Serializer):
    class Meta:
        model = Todo
        fields = ['id', 'description', 'state']

class RestView(metaclass=ABCMeta):
    serializer=None
    def __init__(self):
        self.base=None

    def register(self):
        base=self.base
        app.add_url_rule(base, base, view_func=self.get, methods=['GET'])
        app.add_url_rule(f'{base}/<int:_id>', base+'get', view_func=self.get_one, methods=['GET'])
        app.add_url_rule(base, base+'post', view_func=self.post, methods=['POST'])

    def get(self):
        serializer = self.serializer
        return jsonify({
            'data': serializer.get_all()
        })
    
    def get_one(self, _id):
        serializer = self.serializer
        try:
            return jsonify({
                'data': serializer.get_one(_id)
            })
        except Exception as e:
            return jsonify(e.json()), e.status_code

    def post(self):
        serializer = self.serializer
        try:
            data = serializer.create(request.json)
            print(data)
            return jsonify({
                'data': data
            })
        except Exception as e:
            return jsonify(e.json()), 401

class UserView(RestView):
    serializer = UserSerializer
    def __init__(self):
        super().__init__()
        self.base = '/api/users'

class TodoView(RestView):
    serializer = TodoSerializer
    def __init__(self):
        super().__init__()
        self.base = '/api/todos'

user_view=UserView()
user_view.register()

todo_view=TodoView()
todo_view.register()

if __name__ == '__main__':
    app.run()

