import os
import sys

APP_NAME = "test_web_app"
APP_DESCRIPTION = "web_app for user tests"
APP_LOGO = ""
APP_STRICT = True

APP_PATH = os.path.dirname(__file__)

LOAD_PLUGINS = ["GwUsersWebManager", "GwWebManager", "GwWeb"]

FLASK_DEBUG = False
FLASK_TEMPLATES_AUTO_RELOAD = True

USERS_DB_URL = "sqlite:///"


GROUNDWORK_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'extended': {
            'format': "%(levelname)-8s %(name)-40s - %(asctime)s - %(message)s"
        },
        'debug': {
            'format': "%(name)s - %(asctime)s - [%(levelname)s] - %(module)s:%(funcName)s(%(lineno)s) - %(message)s"
        },
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'level': 'DEBUG'
        },
        'console_stdout': {
            'formatter': 'extended',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': 'DEBUG'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'groundwork': {
            'handlers': ['console_stdout'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}