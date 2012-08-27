from flask import Blueprint, render_template
from package.models import Package, Release

mod = Blueprint('base', __name__)


@mod.route('/')
def index():

    latest = Release.query.order_by(Release.pub_date.desc())
    package_count = Package.query.count()

    return render_template('base/index.html',
        releases=latest,
        package_count=package_count
    )


@mod.route('/package/<package_name>/')
def package(package_name):

    package = Package.query.filter_by(name=package_name).one()
    releases = Release.query.filter_by(package_id=package.id)

    return render_template('base/package.html',
        package=package,
        releases=releases
    )


@mod.route('/package/<package_name>/<version>/')
def release(package_name, version):

    package = Package.query.filter_by(name=package_name).one()
    release = Release.query.filter_by(package_id=package.id, version=version).one()

    return render_template('base/release.html',
        package=package,
        release=release
    )
