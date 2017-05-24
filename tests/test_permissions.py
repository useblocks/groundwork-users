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
