class PermissionViews:
    def __init__(self, plugin):
        self.plugin = plugin

    def overview(self):
        permissions = self.plugin.app.permissions.get_from_db()
        registered_permissions = self.plugin.app.permissions.get_registered().keys()
        return self.plugin.web.render("permission_overview.html",
                                      permissions=permissions, registered_permissions=registered_permissions)

    def detail(self, permission_name):
        permission = self.plugin.app.permissions.get_from_db(permission_name)[0]
        registered_permission = self.plugin.app.permissions.get_registered(permission_name)
        return self.plugin.web.render("permission_detail.html",
                                      permission=permission, registered_permission=registered_permission)

    # def view_permission_overview():
    #     permissions = get_shared_object("Permissions")["shared_object"]
    #     return render_template("usermanager_permission_overview.html", objects=permissions)
    #
    #
    # def view_permission_details(permission_name):
    #     permissions = get_shared_object("Permissions")["shared_object"]
    #     permission_store = get_shared_object("permissionStore")["shared_object"]
    #     if permission_name not in permissions.keys():
    #         abort(404)
    #     permission = permissions[permission_name]
    #     permission_db = permission_store.get_permission_by_name(permission_name)
    #
    #     # Find routes with ths permission
    #     pm = plugin_manager()
    #     plugins = pm.getPluginsOfCategory("Plugin")
    #     decorators = _get_decorators(plugins)
    #     needed_decorators = ["permission_required.<locals>.wrapper", "permission_allowed.<locals>.wrapper"]
    #     found_routes = []
    #     for needed_decorator in needed_decorators:
    #         for route in decorators[needed_decorator]["routes"].keys():
    #             for parameter in decorators[needed_decorator]["routes"][route]["parameters"]:
    #                 if permission_name == parameter or (isinstance(parameter, tuple) and permission_name == parameter[0]):
    #                     found_route = decorators[needed_decorator]["routes"][route].copy()
    #                     found_route["decorator"] = needed_decorator
    #                     found_routes.append(found_route)
    #
    #     return render_template("usermanager_permission_details.html", permission=permission,
    #                            permission_db=permission_db, routes=found_routes)
