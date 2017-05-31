def test_domains_api(users_web_manager):
    assert hasattr(users_web_manager, "domains")
    assert hasattr(users_web_manager.domains, "register")
    assert hasattr(users_web_manager.domains, "get")
    assert hasattr(users_web_manager.domains, "delete")

    app = users_web_manager.app
    assert hasattr(app, "domains")
    assert hasattr(app.domains, "register")
    assert hasattr(app.domains, "get")
    assert hasattr(app.domains, "delete")


def test_domains_creation(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    domain = users_web_manager.domains.register("test_domain", users=[user])
    assert domain is not None
    assert hasattr(domain, "name")


def test_domains_get(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    domain_1 = users_web_manager.domains.register("test_domain", users=[user])
    domains = users_web_manager.domains.get()
    assert len(domains) == 1
    assert domain_1 == domains[0]


def test_domains_delete(users_web_manager):
    user = users_web_manager.users.register("me", "me@me.com", "me-pw")
    domain_1 = users_web_manager.domains.register("test_domain", users=[user])
    domains = users_web_manager.domains.get()
    assert len(domains) == 1

    users_web_manager.domains.delete(domain_1.name)

    domains = users_web_manager.domains.get()
    assert len(domains) == 0
