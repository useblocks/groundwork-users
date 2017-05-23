def test_apikeys_api(users_web_manager):
    assert hasattr(users_web_manager, "apikeys")
    assert hasattr(users_web_manager.apikeys, "register")
    assert hasattr(users_web_manager.apikeys, "get")
    assert hasattr(users_web_manager.apikeys, "delete")

    app = users_web_manager.app
    assert hasattr(app, "apikeys")
    assert hasattr(app.apikeys, "register")
    assert hasattr(app.apikeys, "get")
    assert hasattr(app.apikeys, "delete")


def test_apikeys_creation(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    apikey = users_web_manager.apikeys.register("test_apikey", user=user)
    assert apikey is not None
    assert hasattr(apikey, "key")


def test_apikeys_get(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    apikey_1 = users_web_manager.apikeys.register("test_apikey", user=user)
    apikeys = users_web_manager.apikeys.get()
    assert len(apikeys) == 1
    assert apikey_1 == apikeys[0]


def test_apikeys_delete(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    apikey_1 = users_web_manager.apikeys.register("test_apikey", user=user)
    apikeys = users_web_manager.apikeys.get()
    assert len(apikeys) == 1

    users_web_manager.apikeys.delete(apikey_1.key)

    apikeys = users_web_manager.apikeys.get()
    assert len(apikeys) == 0
