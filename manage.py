#!/usr/bin/env python

from flaskext.script import Manager

from app import app, db
manager = Manager(app)


@manager.command
def createdb(drop=False):

    if drop:
        db.drop_all()

    db.create_all()


@manager.command
def watchreleases():

    from pit.tasks import get_latest_packages

    for release in get_latest_packages():
        print release.name, release.version

if __name__ == "__main__":
    manager.run()
