from app import db


class TestRun(db.Model):

    __tablename__ = 'pit_testrun'

    id = db.Column(db.Integer, primary_key=True)
    release = db.relationship('Release', backref='release', lazy='select')
