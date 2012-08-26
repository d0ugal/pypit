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

    from package.tasks import get_latest_packages
    get_latest_packages.delay()

if __name__ == "__main__":
    manager.run()
