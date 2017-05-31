import pytest


def test_permissions_api(users_web_manager):
    assert hasattr(users_web_manager, "permissions")
    assert hasattr(users_web_manager.permissions, "register")
    assert hasattr(users_web_manager.permissions, "get_registered")
    assert hasattr(users_web_manager.permissions, "get_from_db")

    app = users_web_manager.app
    assert hasattr(app, "permissions")
    assert hasattr(app.permissions, "register")
    assert hasattr(app.permissions, "get_registered")
    assert hasattr(app.permissions, "get_from_db")


def test_permission_registration(users_web_manager):
    permission = users_web_manager.permissions.register("test_permission")
    assert permission is not None
    assert hasattr(permission, "func_name")


def test_permissions_get(users_web_manager):
    permission_1 = users_web_manager.permissions.register("test_permission")
    permission_2 = users_web_manager.permissions.get_from_db(permission_1.name)[0]
    assert permission_1 == permission_2


def test_permission_has_permission(users_web_manager):
    permission = users_web_manager.permissions.register("test_permission")
    user_1 = users_web_manager.users.register("test_user", "user@test.com", "my_password", permissions=[permission])
    user_2 = users_web_manager.users.register("test_user_2", "user_2@test.com", "my_password")
    assert user_1.has_permission(permission.name)
    assert user_2.has_permission(permission.name) is False


def test_permission_has_permission_with_func(users_web_manager):

    def perm_func(permission, return_value, **kwargs):
        return return_value

    permission = users_web_manager.permissions.register("test_permission", func=perm_func)
    user_1 = users_web_manager.users.register("test_user", "user@test.com", "my_password", permissions=[permission])
    user_2 = users_web_manager.users.register("test_user_2", "user_2@test.com", "my_password")

    with pytest.raises(TypeError):
        assert user_1.has_permission(permission.name)

    assert user_1.has_permission(permission.name, return_value=True)
    assert user_1.has_permission(permission.name, return_value=False) is False
    assert user_2.has_permission(permission.name) is False


def test_permission_check(users_web_manager):
    from groundwork_users.patterns.gw_users_pattern.users import UserDoesNotExistException
    from groundwork_users.patterns.gw_users_pattern.permissions import PermissionDoesNotExistException

    def perm_func(permission, return_value, **kwargs):
        return return_value

    permission = users_web_manager.permissions.register("test_permission", func=perm_func)
    user_1 = users_web_manager.users.register("test_user", "user@test.com", "my_password", permissions=[permission])
    user_2 = users_web_manager.users.register("test_user_2", "user_2@test.com", "my_password")

    with pytest.raises(UserDoesNotExistException):
        users_web_manager.app.permissions.check(permission.name, "unknown_user")

    with pytest.raises(PermissionDoesNotExistException):
        users_web_manager.app.permissions.check("unknown_permission", user_1.user_name)

    assert users_web_manager.app.permissions.check(permission.name, user_1.user_name, return_value=True)
    assert users_web_manager.app.permissions.check(permission.name, user_1.user_name, return_value=False) is False
    assert users_web_manager.app.permissions.check(permission.name, user_2.user_name) is False
