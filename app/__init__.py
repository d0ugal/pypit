
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


def create_app():
    return Flask("pypit", template_folder='app/templates',
        static_folder='app/static')

app = create_app()
app.config.from_object('config')

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 404


from app.util.template import format_datetime_filter, nl2br, rst_to_html
app.jinja_env.filters['datetime'] = format_datetime_filter
app.jinja_env.filters['nl2br'] = nl2br
app.jinja_env.filters['rst_to_html'] = rst_to_html

from app import views
app.register_blueprint(views.mod)

from package.models import *
from pit.models import *
