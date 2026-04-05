from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from app.extensions import bcrypt, db
from flask_jwt_extended import JWTManager
from app.services import facade
from sqlalchemy import text

# Import the v1 blueprint-like initializer (namespaces registration)
from app.api.v1 import register_namespaces
jwt = JWTManager()


def create_app(config_class=DevelopmentConfig):
    """
    Application factory.
    Creates and configures the Flask app and registers API namespaces.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Create Flask-RESTX API wrapper.
    # 'doc' defines where Swagger UI will be exposed.
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    # Register v1 namespaces (Presentation Layer)
    register_namespaces(api)


    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        db.create_all()
        #Create admin user using seed method in facade
        facade.seed_admin_user()

    # with app.app_context():
        
    return app
