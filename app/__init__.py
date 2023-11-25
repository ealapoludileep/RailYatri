from flask import Flask, render_template
import os
from .db import init as db
from . import railway


def create_app(test_config=None):
    template_dir = os.path.abspath('./')
    app = Flask(__name__, instance_relative_config=True,
                root_path=template_dir)
    app.config.from_mapping(SECRET_KEY='dev', DATABASE=os.path.join(
        app.instance_path, 'app.sqlite'))

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "Hello World"

    # @app.route('/')
    # def index():
    #     return render_template('base.html')

    db.init_app(app)
    app.register_blueprint(railway.bp)
    app.add_url_rule('/', endpoint='index')
    # flask --app flaskr init-db

    return app
