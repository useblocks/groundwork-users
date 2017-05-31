class RolesPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

    def register(self, name, description=None, permissions=None, users=None):
        return self.app.roles.register(name, description, permissions, users, plugin=self.plugin)

    def get(self, role_name=None, **kwargs):
        return self.app.roles.get(role_name, plugin=self.plugin, **kwargs)

    def delete(self, role_name):
        return self.app.roles.delete(role_name, plugin=self.plugin)


class RolesApplication:
    def __init__(self, app, users_db):
        self.app = app
        self.users_db = users_db

        self.Role = self.users_db.classes.get("Role")
        if self.Role is None:
            raise NoRoleTableException("Database table model 'Role' not found")

    def register(self, name, description=None, permissions=None, users=None, plugin=None):

        if plugin is None:
            raise ValueError("plugin must not be None")

        if permissions is None:
            permissions = []

        if users is None:
            users = []

        role = self.Role(name=name,
                         description=description,
                         permissions=permissions,
                         users=users,
                         plugin_name=plugin.name)
        self.users_db.add(role)
        self.users_db.commit()
        return role

    def get(self, role_name=None, plugin=None, **kwargs):
        if role_name is not None:
            kwargs["name"] = role_name

        if plugin is None:
            roles = self.users_db.query(self.Role).filter_by(**kwargs).all()
        else:
            kwargs["plugin_name"] = plugin.name
            roles = self.users_db.query(self.Role).filter_by(**kwargs).all()

        return roles

    def delete(self, role_name, plugin=None):
        role = self.get(role_name, plugin=plugin)
        if len(role) == 0:
            raise RoleDoesNotExistException("Role {0} does not exist.".format(role_name))
        role = role[0]
        self.users_db.delete(role)
        self.users_db.commit()
        self.app.log.info("Deleted role {0}".format(role.name))


class NoRoleTableException(Exception):
    pass


class RoleDoesNotExistException(Exception):
    pass
