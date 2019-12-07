from sqlalchemy import exc
from main import db

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

