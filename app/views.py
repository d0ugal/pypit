from flask import Blueprint, render_template
from package.models import Package, Release

mod = Blueprint('base', __name__)


@mod.route('/')
def index():

    latest = Release.query.order_by(Release.added).limit(20)

    return render_template('base/index.html', releases=latest)


@mod.route('/package/<package_name>/')
def package(package_name):

    package = Package.query.filter_by(name=package_name).one()

    return render_template('base/package.html', package=package)
