PyPit - Python Package Index Tester
====================================

Testing, validating  and reporting PyPI submissions. Work in progress.

Installation/Running
--------------------

* workon pypit
* add ip6 local trusted connection to postgres config
* add vagrant role to postgres (LOGIN SUPERUSER)
* install redis
* sudo apt-get install libxslt1-dev
* pip install -r requirements.txt
* sudo service postgresql-8.4 restart
* cd /vagrant
* python manage.py createdb
* python manage.py runserver

TODO
----

Fix the provisioning of the VM so most of this is done automatically.

