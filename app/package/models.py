from app import db


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pypi_name = db.Column(db.String(30))
    releases = db.relationship('Release', backref='package', lazy='dynamic')


class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))


"""
    __tablename__ = 'package_release'
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(None, db.ForeignKey('package_package.id'))
    package = db.relation(Package, primaryjoin=(package_id==Package.id),
                 backref=db.backref('buys', order_by=id))


    The following fields are copied verbatim from the PyPI JSON package
    output. For example http://pypi.python.org/pypi/pip/json . We may not want
    everything, so this can be revisited later. Some of it seems useless.
    maintainer = db.Column(db.String(30))
    docs_url = db.Column(db.String(200))
    requires_python = db.Column(db.Boolean)
    maintainer_email = db.Column(db.String(75))
    cheesecake_code_kwalitee_id = db.Column(db.Integer)
    keywords = db.Column(db.String(75))
    package_url = db.Column(db.String(200))
    author = db.Column(db.String(75))
    author_email = db.Column(db.String(75))
    download_url = db.Column(db.String(200))
    platform = db.Column(db.String(30))
    version = db.Column(db.String(10))
    cheesecake_documentation_id = db.Column(db.Integer)
    _pypi_hidden = db.Column(db.Boolean)
    description = db.Column(db.Text)
    release_url = db.Column(db.String(75))
    _pypi_ordering = db.Column(db.Integer)
    classifiers = db.Column(db.Text)
    name = db.Column(db.String(30))
    bugtrack_url = db.Column(db.String(75))
    license = db.Column(db.Text)
    summary = db.Column(db.Text)
    home_page = db.Column(db.String(75))
    stable_version = db.Column(db.String(10))
    cheesecake_installability_id = db.Column(db.String(10))
"""
