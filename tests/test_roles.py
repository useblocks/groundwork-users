def test_roles_api(users_web_manager):
    assert hasattr(users_web_manager, "users")
    assert hasattr(users_web_manager.users, "roles")
    assert hasattr(users_web_manager.users.roles, "register")
    assert hasattr(users_web_manager.users.roles, "get")

    app = users_web_manager.app
    assert hasattr(app, "users")
    assert hasattr(app.users.roles, "register")
    assert hasattr(app.users.roles, "get")


# def test_roles_creation(users_web_manager):
#     role = users_web_manager.users.role.register("test_role")
#     assert role is not None
#     assert hasattr(role, "name")
#
#
# def test_roles_get(users_web_manager):
#     role = users_web_manager.users.roles.register("test_role")
#     role_2 = users_web_manager.users.roles.get("test_role")
#     assert role_2 is not None
#     assert role == role_2
#
#     role_3 = users_web_manager.users.roles.get("unknown_roles")
#     assert role_3 is None
