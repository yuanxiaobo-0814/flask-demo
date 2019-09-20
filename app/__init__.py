
import os
from flask import Flask
from config import config_map
from app.models import db


def create_app(env=None):

    app = Flask(__name__)

    load_config(app, env)

    db.init_app(app)

    register_blueprints(app)

    return app


def load_config(app, env):

    if env is None:
        config_name = os.environ.get('FLASK_ENV')
    else:
        config_name = env

    if config_name is None:
        config_name = 'production'

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)


def register_blueprints(app):

    from app.api.admin import admin_bp
    from app.api.client import client_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)
