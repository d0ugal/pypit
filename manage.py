#!/usr/bin/env python

from flaskext.script import Manager

from app import app, db
manager = Manager(app)


@manager.command
def createdb():
    db.create_all()

if __name__ == "__main__":
    manager.run()
