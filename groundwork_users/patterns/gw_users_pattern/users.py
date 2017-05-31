from flask_security.utils import encrypt_password


class UsersPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

    def register(self, user_name, email, password, full_name="", page=None, description=None,
                 domain=None, groups=None, roles=None, permissions=None, confirmed_at=None, active=True):
        return self.app.users.register(user_name, email, password, full_name, page, description,
                                       self.plugin, domain, groups, roles, permissions, confirmed_at, active)

    def get(self, user_name=None, **kwargs):
        return self.app.users.get(user_name=user_name, plugin=self.plugin, **kwargs)

    def delete(self, user_name):
        return self.app.users.delete(user_name=user_name, plugin=self.plugin)


class UsersApplication:
    def __init__(self, app):
        self.app = app
        self.users_db = app.databases.get("users_db")

        if self.users_db is None:
            raise NoUserDatabaseException("No database 'users_db' found")

        self.User = self.users_db.classes.get("User")
        if self.User is None:
            raise NoUserTableException("Database table model 'User' not found")

    def register(self, user_name, email, password, full_name=None, page=None, description=None,
                 plugin=None, domain=None, groups=None, roles=None, permissions=None, confirmed_at=None, active=True):
        if plugin is None:
            raise ValueError("plugin must not be None")

        if password is not None and len(password) > 0:
            with self.app.web.flask.app_context():
                password_hash = encrypt_password(password)
        else:
            password_hash = ""

        if plugin is None:
            plugin_name = None
        else:
            plugin_name = plugin.name

        if groups is None:
            groups = []

        if roles is None:
            roles = []

        if permissions is None:
            permissions = []

        user = self.User(user_name=user_name, email=email, password=password_hash,
                         full_name=full_name, plugin_name=plugin_name, domain=domain,
                         page=page, description=description, groups=groups,
                         roles=roles, permissions=permissions, confirmed_at=confirmed_at, active=active)
        self.users_db.add(user)
        self.users_db.commit()
        return user

    def delete(self, user_name, plugin=None):
        user = self.get(user_name)
        if len(user) == 0:
            raise UserDoesNotExistException("User {0} does not exist.".format(user_name))
        user = user[0]
        apikeys = self.app.apikeys.get(user=user, plugin=plugin)
        for apikey in apikeys:
            self.app.apikeys.delete(apikey.key)

        self.users_db.delete(user)
        self.users_db.commit()
        self.app.log.info("Deleted user {0}".format(user.user_name))

    def get(self, user_name=None, plugin=None, **kwargs):
        if user_name is not None:
            kwargs["user_name"] = user_name

        if plugin is None:
            users = self.users_db.query(self.User).filter_by(**kwargs).all()
        else:
            kwargs["plugin_name"] = plugin.name
            users = self.users_db.query(self.User).filter_by(**kwargs).all()

        return users


class NoUserDatabaseException(Exception):
    pass


class NoUserTableException(Exception):
    pass


class UserDoesNotExistException(Exception):
    pass
