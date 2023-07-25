# Python Standard Library
import multiprocessing
import os
import pathlib

# Third Party (PyPI) Imports
# `config` is a registered setting for gunicorn
from decouple import config as _config


BASE_DIR = pathlib.Path(__file__).parent

ENV = _config("DJANGO_ENV", default="development", cast=str)
IP_ADDRESS = _config("WSGI_IP_ADDRESS", default="127.0.0.1")
PORT = _config("WSGI_PORT", default=8000, cast=int)
APP_NAME = _config("WSGI_APP_NAME", default="core", cast=str)
LOG_FOLDER = _config("WSGI_LOG_FOLDER", default=".gunicorn", cast=str)
WORKER_LIMIT = _config("WSGI_WORKER_LIMIT", default=1, cast=int)

bind = f"{IP_ADDRESS}:{PORT}"

reload = ENV == "development"

base_name = f"{APP_NAME}_{ENV}"

workers = min(WORKER_LIMIT, multiprocessing.cpu_count() * 2 + 1)

pidfile = os.path.join(BASE_DIR, LOG_FOLDER, "gunicorn.pid")

if ENV == "development":
    # Do not create files in development mode
    accesslog = "-"
    errorlog = "-"

    # Watch for template files change
    excluded_folders_str = _config("WSGI_EXCLUDED_FOLDERS", "")
    excluded_folders = tuple(
        str(BASE_DIR / folder) for folder in excluded_folders_str.split(",")
    )

    template_list = []
    for path, subdirs, files in os.walk(BASE_DIR):
        if not path.startswith(excluded_folders):
            template_list.extend(
                [
                    str(pathlib.PurePath(path, file))
                    for file in files
                    if file.endswith(".html")
                ]
            )
    reload_extra_files = template_list
else:
    accesslog = os.path.join(BASE_DIR, LOG_FOLDER, "gunicorn_access.log")
    errorlog = os.path.join(BASE_DIR, LOG_FOLDER, "gunicorn_error.log")

django_settings = f"{APP_NAME}.settings"

wsgi_app = f"{APP_NAME}.wsgi:application"
