import os

from celery import Celery

from speid import app


def make_celery(app):
    celery_app = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        include=['speid.tasks.orders'],
    )
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


app.config['CELERY_BROKER_URL'] = os.environ['AMPQ_ADDRESS']

celery = make_celery(app)