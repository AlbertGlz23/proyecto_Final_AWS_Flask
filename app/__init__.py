from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.routes.alumnos import alumnos_bp
    from app.routes.profesores import profesores_bp
    app.register_blueprint(alumnos_bp, url_prefix='/alumnos')
    app.register_blueprint(profesores_bp, url_prefix='/profesores')

    with app.app_context():
        db.create_all()

    return app
