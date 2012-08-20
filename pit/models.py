from app import db

from package.models import Release


class TestRun(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('release.id'), nullable=False)
    release = db.relation(Release, primaryjoin=(release_id == Release.id),
                 backref=db.backref('test_runs', order_by=id))
