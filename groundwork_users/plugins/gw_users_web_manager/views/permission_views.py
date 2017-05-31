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
