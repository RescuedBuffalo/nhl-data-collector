from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datacollector.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from datacollector.app.routes import main
    app.register_blueprint(main)

    return app
