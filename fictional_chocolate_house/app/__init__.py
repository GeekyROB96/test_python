from flask import Flask
import os

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))
    app.secret_key = "d4d68adfc046579d752916505b72d581"
    return app