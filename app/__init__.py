from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.celery import Celery


def create_app():
    return Flask("pypit")

app = create_app()
app.config.from_pyfile('config.py')

celery = Celery(app)
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 404

from package.models import *
from pit.models import *
