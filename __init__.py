import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy, Model
from celery import Celery

from app.config import config
from app.errors import CustomException
from app.utils.celery_util import make_celery

# Creating Flask instance.
app = Flask(__name__)

CORS(app, origins="*", supports_credentials=True)

config_name = os.getenv("FLASK_CONFIG") or "default"
app.config.from_object(config[config_name])


class BaseModel(Model):
    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Initializing database and celery instances.
db = SQLAlchemy(app, model_class=BaseModel)
celery = make_celery(app)

# Hooking custom error handler.
@app.errorhandler(CustomException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# TODO: Implement factory
from . import models
from .letter import letter as letter_blueprint

# Registering blueprint.
app.register_blueprint(letter_blueprint, url_prefix="/letter")
