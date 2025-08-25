from flask import Flask
from flask_migrate import Migrate
from config import DevConfig, ProdConfig, TestConfig
from .routes.response import response_bp
from .routes.questions import questions_bp
from .models.response import Response
from .models.questions import Statistic, Question
from app.models import db


config_mapping = {
    'development': DevConfig,
    'production': ProdConfig,
    'resting': TestConfig
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)

    migrate = Migrate() # new
    migrate.init_app(app, db) # new

    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)

    return app
