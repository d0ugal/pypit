from app.celery import celery


@celery.task(name="pit.get_latest_packages", ignore_result=True)
def run_the_gauntlet(release):
    pass
