import os
import pytest


@pytest.fixture()
def app_path(tmpdir_factory):
    session_app_path = tmpdir_factory.mktemp("data").strpath
    session_app_path = os.path.join(session_app_path, "app_path")
    os.mkdir(session_app_path)
    return session_app_path


@pytest.fixture
def web_app(app_path):
    """
    Creates a web-related application for testing

    See https://docs.pytest.org/en/latest/fixture.html#override-a-fixture-with-direct-test-parametrization
    for details of how to override the conf_source location.
    """
    from groundwork import App
    from groundwork_users.plugins import GwUsersWebManager

    configs = app_configs(app_path, os.path.join("configs", "web_app_conf.py"))
    app = App(configs, strict=True)
    user_manager = GwUsersWebManager(app)
    user_manager.activate()
    return app


@pytest.fixture
def web_app_static_db(app_path):
    """
    Creates a web-related application for testing (using a static file db. So values are stored!)

    See https://docs.pytest.org/en/latest/fixture.html#override-a-fixture-with-direct-test-parametrization
    for details of how to override the conf_source location.
    """
    from groundwork import App
    from groundwork_users.plugins import GwUsersWebManager

    configs = app_configs(app_path, os.path.join("configs", "web_file_db_conf.py"))
    print(configs)
    app = App(configs, strict=True)
    user_manager = GwUsersWebManager(app)
    user_manager.activate()
    return app


@pytest.fixture
def users_web_manager(web_app):
    web_manager = web_app.plugins.get("GwUsersWebManager")
    return web_manager


@pytest.fixture
def users_web_manager_static(web_app_static_db):
    web_manager = web_app_static_db.plugins.get("GwUsersWebManager")
    return web_manager


def app_configs(app_path, conf_source):
    """
    Writes a new configuration file, based on the temporary app_path and a manual created config file.
    """
    final_config_path = os.path.join(app_path, "configuration.py")
    with open(final_config_path, "w") as final_config:
        app_path = app_path.replace("\\", "\\\\")
        final_config.write("APP_PATH = \"{0}\"\n".format(app_path))
        final_config.write("LOAD_PLUGINS = []\n")

        with open(os.path.join(os.path.dirname(__file__), conf_source)) as config:
            final_config.write(config.read())

    configs = [final_config_path]
    return configs
