from dateutil.parser import parse
from lxml import etree
from requests import get
from StringIO import StringIO

from app import app, celery
from package.models import Package, Release


@celery.task(name="pit.get_latest_packages", ignore_result=True)
def get_latest_packages():
    """
    Read the PyPI newest packages RSS feed and return a list of the latest
    releases.
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
        release_info = get(properties['link'] + "/json").json

        # remove the wrapping object.
        release = release_info['info']

        # Strip whitespace from string values, there seems to be quite a few
        # newlines etc. dotted around the data that we don't want.
        for k, v in release.items():
            if isinstance(v, basestring):
                release[k] = v.strip()

        releases.append(release)

    for release in releases:
        pass


    return releases


@celery.task(name="pit.get_latest_packages", ignore_result=True)
def run_the_gauntlet(release):
    pass
