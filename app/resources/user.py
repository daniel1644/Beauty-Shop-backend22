from flask_restful import Resource
from flask import request
from app.models import User
from app.schemas import UserSchema
from app import db

class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        schema = UserSchema()
        return schema.dump(user), 200

    def put(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        schema = UserSchema()
        user = schema.load(data, instance=user, partial=True)
        db.session.commit()
        return schema.dump(user), 200

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)
        return schema.dump(users), 200

    def post(self):
        data = request.get_json()
        schema = UserSchema()
        user = schema.load(data)
        db.session.add(user)
        db.session.commit()
        return schema.dump(user), 201
