class GroupsPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

    def register(self, name, description=None, users=None, permissions=None, roles=None):
        return self.app.groups.register(name, description, users,
                                        permissions=permissions, roles=roles, plugin=self.plugin)

    def get(self, group_name=None):
        return self.app.groups.get(group_name, plugin=self.plugin)

    def delete(self, group_name):
        return self.app.groups.delete(group_name, plugin=self.plugin)


class GroupsApplication:
    def __init__(self, app, users_db):
        self.app = app
        self.users_db = users_db

        self.Group = self.users_db.classes.get("Group")
        if self.Group is None:
            raise NoGroupTableException("Database table model 'Group' not found")

    def register(self, name, description=None, users=None, permissions=None, roles=None, plugin=None):
        if plugin is None:
            raise ValueError("plugin must not be None")
        if users is None:
            users = []

        if permissions is None:
            permissions = []

        if roles is None:
            roles = []

        group = self.Group(name=name,
                           description=description,
                           users=users,
                           permissions=permissions,
                           roles=roles,
                           plugin_name=plugin.name)
        self.users_db.add(group)
        self.users_db.commit()
        return group

    def get(self, group_name=None, plugin=None, **kwargs):
        if group_name is not None:
            kwargs["name"] = group_name

        if plugin is None:
            group = self.users_db.query(self.Group).filter_by(**kwargs).all()
        else:
            kwargs["plugin_name"] = plugin.name
            group = self.users_db.query(self.Group).filter_by(**kwargs).all()
        return group

    def delete(self, group_name, plugin=None):
        group = self.get(group_name, plugin=plugin)
        if len(group) == 0:
            raise GroupDoesNotExistException("Group {0} does not exist.".format(group_name))
        group = group[0]
        self.users_db.delete(group)
        self.users_db.commit()
        self.app.log.info("Deleted group {0}".format(group.name))


class NoGroupTableException(Exception):
    pass


class GroupDoesNotExistException(Exception):
    pass
