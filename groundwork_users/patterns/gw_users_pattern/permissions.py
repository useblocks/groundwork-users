class PermissionsPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

    def register(self, name, description=None, func=None, params=None):
        return self.app.permissions.register(name=name, description=description,
                                             func=func, params=params, plugin=self.plugin)

    def get_registered(self, permission_name=None):
        return self.app.permissions.get_registered(permission_name, plugin=self.plugin)

    def get_from_db(self, permission_name=None):
        return self.app.permissions.get_from_db(permission_name, plugin=self.plugin)


class PermissionsApplication:
    def __init__(self, app, users_db):
        self.app = app
        self.users_db = users_db
        self._permissions = {}

        self.Permission = self.users_db.classes.get("Permission")
        if self.Permission is None:
            raise NoPermissionTableException("Database table model 'Permission' not found")

    def register(self, name, description=None, func=None, params=None, plugin=None):
        if plugin is None:
            raise ValueError("plugin must not be None")

        if name in self._permissions.keys():
            raise PermissionExistsException("Permission {0} already registered by plugin {1}".format(
                name, self._permissions[name][name]))

        # Let's store our permission inside a dictionary, because permissions are always defined by developers during
        # plugin/pattern activation. So they are hard coupled to to availability of the plugin, which has performed
        # the registration and maybe is needed to provide the registered func.
        self._permissions[name] = Permission(name=name,
                                             description=description,
                                             func=func,
                                             params=params,
                                             plugin=plugin)

        # Ok, we still need som permission information in our db, because user objects will be mapped to them
        # and the mapping is performed by an administrator, who needs to keep the mapping even if the system restarts.
        try:
            func_name = func.__name__
        except AttributeError:
            func_name = None

        db_permission = self.users_db.query(self.Permission).filter_by(name=name).first()
        # If a permission exists already, we will override it. Maybe a plugin gets exchanged and the new one can
        # reuse the old permission names.
        if db_permission is not None:
            db_permission.description = description
            db_permission.func_name = func_name
            db_permission.func_params = str(params)
            db_permission.plugin = plugin.name
        else:
            db_permission = self.Permission(
                name=name,
                description=description,
                func_name=func_name,
                func_params=str(params),
                plugin_name=plugin.name)

            self.users_db.add(db_permission)
            self.users_db.commit()

        return db_permission

    def get_registered(self, permission_name=None, plugin=None):
        if permission_name is None:
            return self._permissions

        if permission_name not in self._permissions.keys():
            return None

        permission = self._permissions[permission_name]

        if plugin is not None and plugin != permission.plugin:
            return None

        return permission

    def get_from_db(self, permission_name=None, plugin=None, **kwargs):
        if permission_name is not None:
            kwargs["name"] = permission_name

        if plugin is None:
            permission = self.users_db.query(self.Permission).filter_by(**kwargs).all()
        else:
            permission = self.users_db.query(self.Permission).filter_by(**kwargs, plugin_name=plugin.name).all()
        return permission


class Permission:
    def __init__(self, name, plugin, description=None, func=None, params=None):
        self.name = name
        self.plugin = plugin
        self.description = description
        self.func = func
        self.params = params


class NoPermissionTableException(Exception):
    pass


class PermissionExistsException(Exception):
    pass


class PermissionDoesNotExistException(Exception):
    pass
