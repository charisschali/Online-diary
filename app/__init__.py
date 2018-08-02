"""
This module intializes the app and imports all modules required
"""
from flask import Flask, render_template
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import app_config
from app.auth import SingUp, Login
from app.entries import Entries, EntryList

def create_app(config_name):
    "This function creates the app and returns it"
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(app_config[config_name])
    api = Api(app)
    JWTManager(app)
    api.add_resource(SingUp, '/mydiary/v1/auth/register')
    api.add_resource(Login, '/mydiary/v1/auth/login')
    api.add_resource(Entries, '/mydiary/v1/entries')
    api.add_resource(EntryList, '/mydiary/v1/entries/<int:entryId>')

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
