from datetime import datetime
from dateutil.parser import parse
from lxml import etree
from requests import get
from socket import error
from StringIO import StringIO

from app import app, db
from app.celery import celery
from package.models import Package, Release, ReleaseUrl


@celery.task(name="package.get_latest_packages", ignore_result=True)
def get_latest_packages():
    """
    Read the PyPI latest packages RSS and create package and release models
    for each package found. Return a list release models containing only those
    that were created in this run (i.e. the new releases).
    """

    response = get(app.config['PYPI_PACKAGES_RSS'])
    tree = etree.parse(StringIO(response.content))

    releases = []

    for item in tree.xpath('channel/item'):

        # TODO: Switch to the following line in Python 2.7+
        #properties = {child.tag: child.xpath("string()") for child in item}
        properties = dict((child.tag, child.xpath("string()")) for child in item)

        # Convert the datestring to a datetime
        properties['pubDate'] = parse(properties['pubDate'])

        # Fetch the release information from PyPi. There is a risk here that
        # a package could be pushed twice quickly and we get the same version
        # information.
        # TODO: The following line could be more efficient as these gets could
        # be run in parallel
        try:
            release_info = get(properties['link'] + "/json").json
        except error:
            print "FAILED; ", properties['link']
            continue

        # remove the wrapping object in the JSON.
        release = release_info['info']
        urls = release_info['urls']

        # Strip whitespace from string values, there seems to be quite a few
        # newlines dotted around the data that we don't want.
        for k, v in release.items():
            if isinstance(v, basestring):
                release[k] = v.strip()

        # Get the package model if it exists, if it doesn't create it.
        package_model = Package.query.filter_by(name=release['name']).first()

        if not package_model:
            package_model = Package(name=release['name'], added=datetime.now())
            db.session.add(package_model)
            # HACK: Commit at this point so we get the ID for the package
            # model. I think there must be a better way to do this with
            # SQLAlchemy.
            db.session.commit()

        # Get the release model if it exists, if it doesn't create it.
        release_model = Release.query.filter_by(package_id=package_model.id, version=release['version']).first()

        if not release_model:
            release_model = Release(package_id=package_model.id, added=datetime.now(), **release)
            db.session.add(release_model)
            # HACK: Commit at this point so we get the ID for the release
            # model. I think there must be a better way to do this with
            # SQLAlchemy.
            db.session.commit()

            # Only add the release models that are created in this run.
            releases.append(release_model)

            for url in urls:
                url_model = ReleaseUrl(release_id=release_model.id, **url)
                db.session.add(url_model)

    # Finally commit this transaction.
    db.session.commit()

    return releases
