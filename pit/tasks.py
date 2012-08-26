from app.celery import celery
from package.models import Package


@celery.task(name="pit.run_the_gauntlet", ignore_result=True)
def run_the_gauntlet(release):
    p = Package.query.get(release.package_id)
    print "Gauntlet: %s" % p.name
