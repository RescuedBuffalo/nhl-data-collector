from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)

    from models import Team, Player, Game, Record, Season

    with app.app_context():
        db.create_all()

    from app.routes import main
    app.register_blueprint(main)

    return app
