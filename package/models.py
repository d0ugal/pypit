from sqlalchemy.dialects.postgresql import ARRAY

from app import db


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pypi_name = db.Column(db.String(100), unique=True, nullable=False)
    added = db.Column(db.DateTime, nullable=False)


class Release(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    package = db.relation(Package, primaryjoin=(package_id == Package.id),
                 backref=db.backref('packages', order_by=id))
    added = db.Column(db.DateTime, nullable=False)

    # The following fields are copied verbatim from the PyPI JSON package
    #output. For example http://pypi.python.org/pypi/pip/json . We may not want
    #everything, so this can be revisited later. Some of it seems useless.
    maintainer = db.Column(db.String(100))
    docs_url = db.Column(db.String(200))
    requires_python = db.Column(db.Boolean)
    maintainer_email = db.Column(db.String(100))
    cheesecake_code_kwalitee_id = db.Column(db.Integer)
    keywords = db.Column(db.Text)
    package_url = db.Column(db.String(200))
    author = db.Column(db.String(100))
    author_email = db.Column(db.String(100))
    download_url = db.Column(db.String(200))
    platform = db.Column(db.String(100))
    version = db.Column(db.String(20))
    provides = db.Column(ARRAY(db.String(30)))
    cheesecake_documentation_id = db.Column(db.Integer)
    _pypi_hidden = db.Column(db.Boolean)
    description = db.Column(db.Text)
    release_url = db.Column(db.String(100))
    _pypi_ordering = db.Column(db.Integer)
    classifiers = db.Column(db.Text)
    name = db.Column(db.String(100))
    bugtrack_url = db.Column(db.String(100))
    license = db.Column(db.Text)
    summary = db.Column(db.Text)
    home_page = db.Column(db.String(100))
    stable_version = db.Column(db.String(10))
    requires = db.Column(ARRAY(db.String(100)))
    cheesecake_installability_id = db.Column(db.String(20))
