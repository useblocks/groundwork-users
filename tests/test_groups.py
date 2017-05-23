def test_groups_api(users_web_manager):
    assert hasattr(users_web_manager, "groups")
    assert hasattr(users_web_manager.groups, "register")
    assert hasattr(users_web_manager.groups, "get")
    assert hasattr(users_web_manager.groups, "delete")

    app = users_web_manager.app
    assert hasattr(app, "groups")
    assert hasattr(app.groups, "register")
    assert hasattr(app.groups, "get")
    assert hasattr(app.groups, "delete")


def test_groups_creation(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    group = users_web_manager.groups.register("test_group", users=[user])
    assert group is not None
    assert hasattr(group, "name")


def test_groups_get(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    group_1 = users_web_manager.groups.register("test_group", users=[user])
    groups = users_web_manager.groups.get()
    assert len(groups) == 1
    assert group_1 == groups[0]


def test_groups_delete(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    group_1 = users_web_manager.groups.register("test_group", users=[user])
    groups = users_web_manager.groups.get()
    assert len(groups) == 1

    users_web_manager.groups.delete(group_1.name)

    groups = users_web_manager.groups.get()
    assert len(groups) == 0
