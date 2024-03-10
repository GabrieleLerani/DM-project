from flask import Flask
from webapp.presentation.controller import main
import os
from dotenv import load_dotenv


def create_app():

    # create flask application
    app = Flask(__name__)
    
    # register the blueprint component
    app.register_blueprint(main)

    # load flask secret key
    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY")
    

    return app
