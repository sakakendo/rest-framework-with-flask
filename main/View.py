from flask import jsonify, request
from abc import ABCMeta
from main import app


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
            print(e)
            return jsonify(e.json()), 401

