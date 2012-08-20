import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset([''])
SECRET_KEY = ''

SQLALCHEMY_DATABASE_URI = "postgresql://localhost/pypit"
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = ""

PYPI_PACKAGES_RSS = 'http://pypi.python.org/pypi?%3Aaction=packages_rss'

try:
    from local_config import *
except ImportError:
    pass
