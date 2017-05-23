import os
from groundwork import App


def start_app():
    config_path = os.path.join(os.path.dirname(__file__), "../configs/users_app_conf.py")
    app = App([config_path], strict=True)
    app.plugins.activate(app.config.get("LOAD_PLUGINS"))

    # User registration
    me = app.users.register("me", "me@me.com", "me_pw", full_name="Me Me_Name", plugin=app)
    daniel = app.users.register("daniel", "dw@useblocks.com", "dw_pw", full_name="Daniel Woste", plugin=app)
    marco = app.users.register("marco", "mh@useblocks.com", "mh_pw", full_name="Marco Heinemann", plugin=app)

    # Domain registration
    app.domains.register("empty_domain", plugin=app)
    app.domains.register("full_domain", users=[marco, daniel], plugin=app)

    # Apikey registration
    app.apikeys.register(user=daniel, plugin=app)
    app.apikeys.register(user=marco, active=False, plugin=app)
    app.apikeys.register(user=marco, plugin=app)

    # Group registration
    app.groups.register("full_group", users=[marco, daniel], plugin=app)
    app.groups.register("empty_group", plugin=app)

    # Permission registration
    app.permissions.register("permission_no_func", plugin=app)
    app.permissions.register("permission_with_func", func=_permission_func, plugin=app)

    app.commands.start_cli()


def _permission_func(**kargs):
    return True

if "main" in __name__:
    start_app()
