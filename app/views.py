from flask import Blueprint, render_template
from package.models import Package, Release
from sqlalchemy import func

from app import db

mod = Blueprint('base', __name__)


@mod.route('/')
def index():

    latest = Release.query.filter(Release.pub_date != None).order_by(Release.pub_date.desc())
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


@mod.route('/stats/')
def stats():

    total = func.count(Release.name).label('total')
    most_releases = db.session.query(Package, total)\
        .join(Release)\
        .group_by(Package.name, Package.id)\
        .order_by("total DESC")\
        .limit(10)

    total = func.count(Release.author).label('total')
    active_author = db.session.query(Release.author, total)\
        .group_by(Release.author)\
        .order_by("total DESC")\
        .limit(10)

    stats = {
        "Packages with most releases": ["%s: %s" % (k.name, v) for k, v in most_releases],
        "Most Frequent Author Name": ["%s: %s" % (k, v) for k, v in active_author],
    }

    return render_template('base/stats.html',
        stats=stats
    )
