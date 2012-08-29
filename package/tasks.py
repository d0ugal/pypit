from datetime import datetime
from dateutil.parser import parse
from lxml import etree
from requests import get
from socket import error as SocketError
from StringIO import StringIO
from urllib2 import URLError
from yolk.cli import CheeseShop, Yolk

from app import app
from app.celery import celery
from app.util.db import get_or_create
from package.models import Package, Release, ReleaseUrl


@celery.task(name="package.get_latest_packages", ignore_result=True)
def get_latest_packages():
    """
    Real the PyPI RSS feed for latest package releases. Create sub tasks to
    fetch and process each release.
    """

    try:
        response = get(app.config['PYPI_PACKAGES_RSS'])
    except SocketError, e:
        raise get_latest_packages.retry(exc=e)

    tree = etree.parse(StringIO(response.content))

    # This is a bit odd, we don't really care, but its easier in the logs if
    # we go through the packages chronologically (in RSS the newest is first
    # but we want the oldest first.)
    for item in reversed(list(tree.xpath('channel/item'))):

        # Convert into simple dict.
        properties = dict((child.tag, unicode(child.xpath("string()"))) for child in item)
        # Convert the datestring to a datetime and create the json url.
        pub_date = parse(properties['pubDate'])
        package_url = properties['link'] + "/json"
        # trigger sub task.
        get_package.delay(package_url, pub_date)


@celery.task(name="package.get_package", ignore_result=True)
def get_package(package_url, pub_date=None):
    """
    Given a release url download it and create the package and release models
    as required. If we create the package for the first time trigger a sub
    task to find old versions and fetch those.

    The passed in pub_date is a bit weird, its a leftover relic from RSS. We
    only have the date if we are adding from RSS, if its an old version we
    don't know it.
    """

    try:
        release_info = get(package_url).json
    except SocketError, e:
        raise get_package.retry(exc=e)

    # remove the wrapping object in the JSON.
    release = release_info['info']
    urls = release_info['urls']

    # Strip whitespace from string values, there seems to be quite a few
    # newlines dotted around the data that we don't want.
    for k, v in release.items():
        if isinstance(v, basestring):
            release[k] = v.strip()

    # Create the Package and Realse models if we don't already have them.
    package_model, package_created = get_or_create(Package, name=release['name'],
        defaults={'added': datetime.now()})

    # If we just created the package then go and get its old versions...
    if package_created:
        backdate_versions.delay(release['name'], release['version'])

    release['added'] = datetime.now()
    release['pub_date'] = pub_date
    release_model, release_created = get_or_create(Release, package_id=package_model.id,
        version=release['version'], defaults=release)

    # store each url in the realse
    if release_created:

        for url in urls:
            get_or_create(ReleaseUrl, release_id=release_model.id, **url)

    return release, release_created


@celery.task(name="package.backdate_versions", ignore_result=True, default_retry_delay=60)
def backdate_versions(package_name, skip_version=None):
    """
    Using some hacky code to use Yolk for what its not designed, get all the
    versions for a package and skip the current one we found in the RSS (we
    are already looking into that). Create sub task to get the old releases.
    """
    y = Yolk()
    y.pkg_spec = [package_name]
    y.pypi = CheeseShop(True)
    try:
        _, _, versions = y.parse_pkg_ver(False)
    except URLError, e:
        raise backdate_versions.retry(exc=e)

    if skip_version and skip_version in versions:
        versions.remove(skip_version)

    package = Package.query.filter_by(name=package_name).one()

    for version in versions:

        # Check we don't already have this version stored.
        q = Release.query
        count = q.filter_by(package_id=package.id, version=version).count()

        if count > 0:
            continue

        package_url = "http://pypi.python.org/pypi/%s/%s/json" % (package_name, version)
        get_package.delay(package_url)


@celery.task(name="package.add_package", ignore_result=True)
def add_package(package_name):

    # Check we don't already have this package. If we do nothing needs done.
    if Package.query.filter_by(name="Django").count() > 0:
        return

    url = "http://pypi.python.org/pypi/%s/json" % package_name

    try:
        response = get(url)
    except SocketError, e:
        raise add_package.retry(exc=e)

    # If we don't get JSON back it means its a registered name with no
    # releases. So just store the package name and stop.
    if not response.json:
        get_or_create(Package, name=package_name, defaults={'added': datetime.now()})
        return

    version = response.json['info']['version']

    package_url = "http://pypi.python.org/pypi/%s/%s/json" % (package_name, version)
    get_package.delay(package_url)


@celery.task(name="package.load_all_pypi_packages", ignore_result=True)
def load_all_pypi_packages():
    """
    Get all of the packages from pypi and run the backdate task on them. This
    will create a huge number of tasks.
    """

    try:
        response = get("http://pypi.python.org/simple/")
    except SocketError, e:
        raise load_all_pypi_packages.retry(exc=e)

    tree = etree.parse(StringIO(response.content))

    for anchor in tree.xpath("body/a"):
        package_name = anchor.xpath("string()")
        add_package.delay(unicode(package_name))
