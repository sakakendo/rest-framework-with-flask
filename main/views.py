from flask import Flask, jsonify, request
from flask.views import MethodView
from main import app
from main import db
from main.exception import(
    NotFound,APIBaseError
)
from main.serializer import Serializer
from main.View import RestView
# import main.models
from main.models import (
    User,
    Todo,
    File
)

API_BASE = ''

class UserSerializer(Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TodoSerializer(Serializer):
    class Meta:
        model = Todo
        fields = ['id', 'description', 'state']


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

'''
@app.route('/api/files', methods=['POST'])
def file_uploader():
    model =  File.create()
    db.session.add(model)
    db.session.commit()
    '''
