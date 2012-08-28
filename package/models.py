from sqlalchemy.dialects.postgresql import ARRAY

from app import db


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    added = db.Column(db.DateTime, nullable=False)


class Release(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    package = db.relation(Package, primaryjoin=(package_id == Package.id),
                 backref=db.backref('packages', order_by=id))
    added = db.Column(db.DateTime, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=True)

    # The following fields are copied verbatim from the PyPI JSON package
    #output. For example http://pypi.python.org/pypi/pip/json . We may not want
    #everything, so this can be revisited later. Some of it seems useless.
    maintainer = db.Column(db.String(200))
    docs_url = db.Column(db.String(300))
    requires_python = db.Column(db.Boolean)
    maintainer_email = db.Column(db.String(200))
    cheesecake_code_kwalitee_id = db.Column(db.Integer)
    keywords = db.Column(db.Text)
    package_url = db.Column(db.String(300))
    author = db.Column(db.String(200))
    author_email = db.Column(db.String(200))
    download_url = db.Column(db.String(300))
    platform = db.Column(db.String(200))
    version = db.Column(db.String(200))
    provides = db.Column(ARRAY(db.String(200)))
    cheesecake_documentation_id = db.Column(db.Integer)
    _pypi_hidden = db.Column(db.Boolean)
    description = db.Column(db.Text)
    release_url = db.Column(db.String(300))
    _pypi_ordering = db.Column(db.Integer)
    classifiers = db.Column(db.Text)
    name = db.Column(db.String(200))
    bugtrack_url = db.Column(db.String(300))
    license = db.Column(db.Text)
    summary = db.Column(db.Text)
    home_page = db.Column(db.String(200))
    stable_version = db.Column(db.String(200))
    requires = db.Column(ARRAY(db.String(200)))
    cheesecake_installability_id = db.Column(db.String(200))


class ReleaseUrl(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('release.id'), nullable=False)
    release = db.relation(Release, primaryjoin=(release_id == Release.id),
                 backref=db.backref('release_urls', order_by=id))

    has_sig = db.Column(db.Boolean)
    upload_time = db.Column(db.DateTime())
    comment_text = db.Column(db.Text())
    python_version = db.Column(db.String(20))
    url = db.Column(db.String(300))
    md5_digest = db.Column(db.String(32))
    downloads = db.Column(db.Integer)
    filename = db.Column(db.String(100))
    packagetype = db.Column(db.String(20))
    size = db.Column(db.Integer)
