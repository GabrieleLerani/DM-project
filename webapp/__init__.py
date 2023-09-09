from flask import Flask

def create_app():
    app = Flask(__name__)
    from .app import main

    # register the blueprint component
    app.register_blueprint(main)
    
    return app
