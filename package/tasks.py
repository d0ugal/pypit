from datetime import datetime
from dateutil.parser import parse
from lxml import etree
from requests import get
from socket import error as SocketError
from StringIO import StringIO

from app import app, db
from app.celery import celery
from app.util.db import get_or_create
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
        try:
            release_info = get(properties['link'] + "/json").json
        except SocketError:
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

        # Create the Package and Realse models if we don't already have them.
        package_model, _ = get_or_create(Package, name=release['name'],
            defaults={'added': datetime.now()})

        release['added'] = datetime.now()
        release_model, release_created = get_or_create(Release, package_id=package_model.id,
            version=release['version'], defaults=release)

        if release_created:

            releases.append(release_model)

            for url in urls:
                get_or_create(ReleaseUrl, release_id=release_model.id, **url)

    return releases
