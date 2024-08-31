from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models import User
from app.schemas import UserSchema
from app import db

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        schema = UserSchema()
        user = schema.load(data)
        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully"}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Ensure to use hashed password in production
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        
        return {"message": "Invalid credentials"}, 401

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        # Currently, this endpoint does nothing but can be used for logging out
        return {"message": "Logout successful"}, 200
