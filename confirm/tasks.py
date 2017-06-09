import shutil
from affirmative.celery import app


@app.task
def copy_to_destination(src, dst):
    try:
        shutil.copytree(src, dst)
    except NotADirectoryError:
        shutil.copy(src, dst)
