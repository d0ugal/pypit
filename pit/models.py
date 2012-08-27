from flask.ext.sqlalchemy import models_committed

from app import app, db
from package.models import Release
from pit.tasks import run_the_gauntlet


class TestRun(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('release.id'), nullable=False)
    release = db.relation(Release, primaryjoin=(release_id == Release.id),
                 backref=db.backref('test_runs', order_by=id))


def on_release_commit(sender, changes):
    for model, change in changes:
        if isinstance(model, Release):
            if model:
                run_the_gauntlet.delay(model)
            else:
                print "False? %s" % model

models_committed.connect(on_release_commit, sender=app)
