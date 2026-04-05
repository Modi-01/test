from flask import Flask
from flask_restx import Api

# Import the v1 blueprint-like initializer (namespaces registration)
from app.api.v1 import register_namespaces


def create_app():
    """
    Application factory.
    Creates and configures the Flask app and registers API namespaces.
    """
    app = Flask(__name__)

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

    return app
