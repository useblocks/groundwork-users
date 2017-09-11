import os
import pytest
from tests.conftest import app_configs


def test_users_api(users_web_manager):
    assert hasattr(users_web_manager, "users")
    assert hasattr(users_web_manager.users, "register")
    assert hasattr(users_web_manager.users, "get")

    app = users_web_manager.app
    assert hasattr(app, "users")
    assert hasattr(app.users, "register")
    assert hasattr(app.users, "get")


def test_users_creation(users_web_manager):
    user = users_web_manager.users.register("test_user", "user@test.com", "my_password")
    assert user is not None
    assert hasattr(user, "user_name")
    assert hasattr(user, "email")
    assert hasattr(user, "full_name")


def test_users_creation_static(users_web_manager_static):
    """
    Makes tests with the existing database "test_web.db", which already have existing users.
    """
    from sqlalchemy.exc import IntegrityError
    with pytest.raises(IntegrityError):
        users_web_manager_static.users.register("test_user", "user@test.com", "my_password")


def test_creation_during_activation(app_path):
    """
    Tests the registration of users already during plugin activation

    :param app_path:
    :return:
    """
    from groundwork import App
    from groundwork_users.patterns import GwUsersPattern

    class MyUserPlugin(GwUsersPattern):
        def __init__(self, app, *args, **kwargs):
            self.name = "MyUserPlugin"
            super(MyUserPlugin, self).__init__(app, *args, **kwargs)
            self.my_user = None

        def activate(self):
            self.my_user = self.users.register("test_user_new", "user_new@test.com", "my_password_new")

    configs = app_configs(app_path, os.path.join("configs", "web_app_conf.py"))
    app = App(configs, strict=True)
    user_manager = MyUserPlugin(app)
    user_manager.activate()
    assert hasattr(user_manager, "my_user")
    assert user_manager.my_user is not None
    assert hasattr(user_manager.my_user, "user_name")


def test_users_get(users_web_manager):
    user = users_web_manager.users.register("test_user", "user@test.com", "my_password")
    user_2 = users_web_manager.users.get("test_user")
    assert user_2 is not None
    assert user == user_2[0]

    user_3 = users_web_manager.users.get("unknown_user")
    assert len(user_3) == 0

    user_4 = users_web_manager.users.get(email="user@test.com")[0]
    assert user == user_4


def test_users_delete(users_web_manager):
    user = users_web_manager.users.register("test_user", "user@test.com", "my_password")
    users = users_web_manager.users.get()
    assert len(users) == 2

    users_web_manager.users.delete(user.user_name)
    users = users_web_manager.users.get()
    assert len(users) == 1


def test_users_apikey_delete(users_web_manager):
    user = users_web_manager.users.register("test_user", "user@test.com", "my_password")
    users_web_manager.apikeys.register("test_apikey", user=user)

    users = users_web_manager.users.get()
    assert len(users) == 2
    apikeys = users_web_manager.apikeys.get()
    assert len(apikeys) == 1

    users_web_manager.users.delete(user.user_name)

    users = users_web_manager.users.get()
    assert len(users) == 1
    apikeys = users_web_manager.apikeys.get()
    assert len(apikeys) == 0
