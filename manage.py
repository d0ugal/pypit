#!/usr/bin/env python

from flaskext.script import Manager

from app import app, db
manager = Manager(app)


@manager.command
def createdb(drop=False):
    """
    Create the initial database structure.
    """

    if drop:
        db.drop_all()

    db.create_all()


@manager.command
def add_package(name):
    """
    Add a particular package to PyPit. Useful for local testing.
    """

    from package.tasks import backdate_versions
    backdate_versions.delay(name)


@manager.command
def load_pypi():
    """
    Very slow and intensive, will create many tasks (around 50,000.)
    """

    from package.tasks import load_all_pypi_packages
    load_all_pypi_packages.delay()

if __name__ == "__main__":
    manager.run()
