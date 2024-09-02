from flask_restful import Resource
from flask import request, make_response, jsonify
from app.models import User
from app.schemas import UserSchema
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        schema = UserSchema()
        response = make_response(jsonify(schema.dump(user)), 200)
        return response

    def put(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        schema = UserSchema()
        try:
            user = schema.load(data, instance=user, partial=True)
            db.session.commit()
            response = make_response(jsonify(schema.dump(user)), 200)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response

    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()
            response = make_response('', 204)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response



class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)
        response = make_response(jsonify(schema.dump(users)), 200)
        return response

    def post(self):
        data = request.get_json()
        schema = UserSchema()
        try:
            # Check if the user already exists
            if User.query.filter_by(email=data.get('email')).first():
                return make_response(jsonify({"error": "User already exists"}), 400)
            
            # Hash the password before storing it
            hashed_password = generate_password_hash(data['password'], method='sha256')
            data['password'] = hashed_password
            
            user = schema.load(data)
            db.session.add(user)
            db.session.commit()
            response = make_response(jsonify(schema.dump(user)), 201)
        except Exception as e:
            db.session.rollback()
            response = make_response(jsonify({"error": str(e)}), 400)
        return response
