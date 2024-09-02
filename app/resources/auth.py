from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.schemas import UserSchema
from app import db

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        schema = UserSchema()
        try:
            # Validate input and create user
            user_data = schema.load(data)
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=generate_password_hash(user_data['password'])  # Hash password
            )
            db.session.add(user)
            db.session.commit()
            return {"message": "User registered successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 400

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')  # Changed 'username' to 'email'
        password = data.get('password')
        
        # Find the user in the database by email
        user = User.query.filter_by(email=email).first()  # Changed 'username' to 'email'
        
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401
        
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200
class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        print(f"User trying to logout: {current_user}")
        return {"message": "Logout successful"}, 200