def test_permissions_api(users_web_manager):
    assert hasattr(users_web_manager, "permissions")
    assert hasattr(users_web_manager.permissions, "register")
    assert hasattr(users_web_manager.permissions, "get")

    app = users_web_manager.app
    assert hasattr(app, "permissions")
    assert hasattr(app.permissions, "register")
    assert hasattr(app.permissions, "get")


def test_permission_registration(users_web_manager):
    permission = users_web_manager.permissions.register("test_permission")
    assert permission is not None
    assert hasattr(permission, "func")


def test_permissions_get(users_web_manager):
    permission_1 = users_web_manager.permissions.register("test_permission")
    permission_2 = users_web_manager.permissions.get(permission_1.name)
    assert permission_1 == permission_2

# def test_permissions_creation(users_web_manager):
#     permission = users_web_manager.users.permission.register("test_permission")
#     assert permission is not None
#     assert hasattr(permission, "name")
#
#
# def test_permissions_get(users_web_manager):
#     permission = users_web_manager.users.permissions.register("test_permission")
#     permission_2 = users_web_manager.users.permissions.get("test_permission")
#     assert permission_2 is not None
#     assert permission == permission_2
#
#     permission_3 = users_web_manager.users.permissions.get("unknown_permissions")
#     assert permission_3 is None
