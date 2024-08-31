# app/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Change this to a real secret key
    SECRET_KEY = 'another_secret_key'  # Secret key for session management
    SESSION_TYPE = 'filesystem'  # Server-side session storage
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
