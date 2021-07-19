import atexit
import os
import shutil
import tempfile

from django.conf import settings


# @pytest.fixture(scope="session", autouse=True)
def pytest_configure():
    kobo_root = tempfile.mkdtemp(suffix="django_kobo_exporter_test")
    atexit.register(shutil.rmtree, path=kobo_root, ignore_errors=True)

    settings.configure(
        ROOT_URLCONF="tests.test_app.urls",
        XMLRPC_METHODS=[],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(kobo_root, "db.sqlite"),
            },
        },
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "kobo.hub.middleware.WorkerMiddleware",
        ],
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            # "kobo.django.auth",
            "kobo.hub",
            "kobo_exporter",
        ],
        TASK_DIR=os.path.join(kobo_root, "tasks"),
        UPLOAD_DIR=os.path.join(kobo_root, "uploads"),
    )
