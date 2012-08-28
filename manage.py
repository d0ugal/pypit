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
def watch_releases():
    """
    Trigger the task to fetch new packages from PyPI.
    """

    from package.tasks import get_latest_packages
    get_latest_packages.delay()


@manager.command
def add_package(name):
    """
    Add a particular package to PyPit. Useful for local testing.
    """

    from package.tasks import backdate_versions
    backdate_versions.delay(name)


@manager.command
def load_all_pypi_packages():
    """
    This will be very slow and create a huge number of tasks.
    """

    from package.tasks import load_all_pypi_packages
    load_all_pypi_packages.delay()

if __name__ == "__main__":
    manager.run()
