from app.celery import celery


@celery.task(name="pit.run_the_gauntlet", ignore_result=True)
def run_the_gauntlet(release):
    pass
