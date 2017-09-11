import os

APP_NAME = "test_web_app"
APP_DESCRIPTION = "web_app for user tests"
APP_LOGO = ""

APP_PATH = os.path.dirname(__file__)

PLUGINS = []

USERS_DB_URL = "sqlite:///{0}".format(os.path.join(os.path.basename(__file__), "../db/test_web.db"))
