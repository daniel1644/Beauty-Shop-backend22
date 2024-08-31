# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_session import Session

# Define metadata with custom naming convention
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Instantiate db and migrate
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize REST API
    api = Api(app)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize Flask-Session
    Session(app)


    # Add a simple route for the root URL
    @app.route('/')
    def index():
        return "Welcome to the Beauty Shop API!"

    # Import and add resources
    from app.resources.product import ProductResource, ProductListResource
    from app.resources.cart import CartResource, CartListResource
    from app.resources.user import UserResource, UserListResource
    from app.resources.order import OrderResource, OrderListResource
    from app.resources.auth import LoginResource, RegisterResource, LogoutResource

    api.add_resource(ProductListResource, '/products')
    api.add_resource(ProductResource, '/products/<int:id>')
    api.add_resource(CartListResource, '/cart')
    api.add_resource(CartResource, '/cart/<int:id>')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<int:id>')
    api.add_resource(OrderListResource, '/orders')
    api.add_resource(OrderResource, '/orders/<int:id>')
    api.add_resource(LoginResource, '/login')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(LogoutResource, '/logout')
    

    return app
