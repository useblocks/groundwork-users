class RolesPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

    def register(self):
        return self.app.users.roles.register(plugin=self.plugin)

    def get(self):
        return self.app.users.roles.get(plugin=self.plugin)


class RolesApplication:
    def __init__(self, app, users_db):
        self.app = app
        self.users_db = users_db

        self.Role = self.users_db.classes.get("Role")
        if self.Role is None:
            raise NoRoleTableException("Database table model 'Role' not found")

    def register(self, plugin=None):
        if plugin is None:
            raise ValueError("plugin must not be None")
        role = self.Role(plugin=plugin.name)
        self.users_db.add(role)
        self.users_db.commit()
        return role

    def get(self, plugin=None):
        if plugin is None:
            role = self.users_db.query(self.Role).filter_by().first()
        else:
            role = self.users_db.query(self.Role).filter_by(plugin=plugin.name).first()
        return role


class NoRoleTableException(Exception):
    pass
