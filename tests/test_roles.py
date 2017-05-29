def test_roles_api(users_web_manager):
    assert hasattr(users_web_manager, "roles")
    assert hasattr(users_web_manager.roles, "register")
    assert hasattr(users_web_manager.roles, "get")
    assert hasattr(users_web_manager.roles, "delete")

    app = users_web_manager.app
    assert hasattr(app, "roles")
    assert hasattr(app.roles, "register")
    assert hasattr(app.roles, "get")
    assert hasattr(app.roles, "delete")


def test_roles_creation(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    permission = users_web_manager.permissions.register("my_permission")
    role = users_web_manager.roles.register("test_role", "my role desc", users=[user], permissions=[permission])
    assert role is not None
    assert hasattr(role, "name")
    assert user in role.users
    assert permission in role.permissions


def test_roles_get(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    role_1 = users_web_manager.roles.register("test_role", users=[user])
    roles = users_web_manager.roles.get()
    assert len(roles) == 2
    assert role_1 == roles[1]


def test_roles_delete(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    role_1 = users_web_manager.roles.register("test_role", users=[user])
    roles = users_web_manager.roles.get()
    assert len(roles) == 2

    users_web_manager.roles.delete(role_1.name)

    roles = users_web_manager.roles.get()
    assert len(roles) == 1

