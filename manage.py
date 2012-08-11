#!/usr/bin/env python

from flaskext.script import Manager

from app import app, db
manager = Manager(app)


@manager.command
def createdb(drop=False):
    if drop:
        db.drop_all()
    db.create_all()

    from app.package.models import Package
    print list(Package.query.filter_by(pypi_name="Django"))


@manager.command
def watchreleases():
    from app.pit.tasks import get_latest_packages

    for package, release in get_latest_packages():
        print release.package.name, release.version

if __name__ == "__main__":
    manager.run()
