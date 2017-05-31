import os

from flask_login import current_user

from groundwork_web.patterns import GwWebPattern

from groundwork_users.patterns import GwUsersPattern
from groundwork_users.plugins.gw_users_web_manager.views.user_views import UserViews
from groundwork_users.plugins.gw_users_web_manager.views.domain_views import DomainViews
from groundwork_users.plugins.gw_users_web_manager.views.apikey_views import ApiKeyViews
from groundwork_users.plugins.gw_users_web_manager.views.group_views import GroupViews
from groundwork_users.plugins.gw_users_web_manager.views.permission_views import PermissionViews
from groundwork_users.plugins.gw_users_web_manager.views.role_views import RoleViews


def belongs_current_user(permission_name, user_name=None, **kwargs):
    """
    Checks if the user-strings (which is unique in the system) belongs to the current user.
    Great to check, if an object (user, node, ...) belongs to current user

    :param user_name: user-string
    :param permission_name: name of the permission
    :return: True, if user-string belongs to current user. Else False.
    """
    if user_name is None:
        return True

    if current_user.user_name == user_name:
        return True
    return False


conf_belongs_current_user = {"func": belongs_current_user,
                             "params": {"user_name": "Name of the user, which belongs the secured object"}}


class GwUsersWebManager(GwUsersPattern, GwWebPattern):
    def __init__(self, app, *args, **kwargs):
        self.name = self.__class__.__name__
        super(GwUsersWebManager, self).__init__(app, *args, **kwargs)
        self.users_db = None
        self.user_model = None
        self.permission_model = None
        self.role_model = None
        self.domain_model = None
        self.apikey_model = None
        self.group_model = None
        self._user_menu = None
        self._login_menu = None
        self._base_dir = os.path.dirname(__file__)
        self._template_folder = os.path.join(self._base_dir, "templates")
        self._static_folder = os.path.join(self._base_dir, "static")

    def activate(self):
        self.users_db = self.databases.get("users_db")
        self.user_model = self.users_db.classes.get("User")
        self.permission_model = self.users_db.classes.get("Permission")
        self.role_model = self.users_db.classes.get("Role")
        self.domain_model = self.users_db.classes.get("Domain")
        self.apikey_model = self.users_db.classes.get("Apikey")
        self.group_model = self.users_db.classes.get("Group")

        self._user_menu = self.web.menus.register("User Manager", "/user/")
        self._login_menu = self.web.menus.register("Login", "bla", link_text="test_me", func=self._login_menu_view)

        self.activate_user()
        self.activate_domain()
        self.activate_apikey()
        self.activate_group()
        self.activate_permission()
        self.activate_role()

    def _login_menu_view(self):
        return self.web.render("user_button.html")

    def activate_user(self):
        views = UserViews(self)
        prefix_url = "/user"
        context = self.web.contexts.register(name="user",
                                             template_folder=self._template_folder,
                                             static_folder=self._static_folder,
                                             url_prefix=prefix_url,
                                             description="Context for user related objects and actions."
                                             )
        self.web.routes.register("/", ["GET"], endpoint=views.overview,
                                 context=context.name, description="Show all registered users")
        self._user_menu.register("Users", prefix_url)

        self.web.routes.register("/<user_name>", ["GET"], endpoint=views.detail,
                                 name="view_user_detail",
                                 context=context.name, description="Shows details of a user")

        self.web.routes.register("/add", ["GET", "POST"], endpoint=views.add,
                                 name="view_user_add",
                                 context=context.name, description="Shows mask for adding new user")

        self.web.routes.register("/edit/<user_name>", ["GET", "POST"], endpoint=views.edit,
                                 name="view_user_edit",
                                 context=context.name, description="Shows mask for editing an existing user")

        self.web.routes.register("/delete/<user_name>", ["GET"], endpoint=views.delete,
                                 name="view_user_delete",
                                 context=context.name, description="Deletes an user")

        # Permission registration
        self.permissions.register("user_view_all", description="User is allowed to view ALL user profiles")
        self.permissions.register("user_edit_all", description="User is allowed to edit ALL user profiles ")
        self.permissions.register("user_delete_all", description="User is allowed to delete ANY user")

        self.permissions.register("user_view_own", description="User is allowed to view OWN user profile",
                                  **conf_belongs_current_user)
        self.permissions.register("user_edit_own", description="User is allowed to edit OWN user profile",
                                  **conf_belongs_current_user)
        self.permissions.register("user_delete_own", description="User is allowed to delete OWN user",
                                  **conf_belongs_current_user)

        self.permissions.register("user_create", description="User is allowed to create new users")

    def activate_domain(self):
        views = DomainViews(self)
        prefix_url = "/domain"
        context = self.web.contexts.register(name="domain",
                                             template_folder=self._template_folder,
                                             static_folder=self._static_folder,
                                             url_prefix=prefix_url,
                                             description="Context for domain related objects and actions."
                                             )

        self.web.routes.register("/", ["GET"], endpoint=views.overview, name="view_domains",
                                 context=context.name, description="Show all registered domains")
        self._user_menu.register("Domains", prefix_url)

        self.web.routes.register("/<domain_name>", ["GET"], endpoint=views.detail,
                                 name="view_domain_detail",
                                 context=context.name, description="Shows details of a domain")

        self.web.routes.register("/add", ["GET", "POST"], endpoint=views.add,
                                 name="view_domain_add",
                                 context=context.name, description="Shows mask for adding new domain")

        self.web.routes.register("/edit/<domain_name>", ["GET", "POST"], endpoint=views.edit,
                                 name="view_domain_edit",
                                 context=context.name, description="Shows mask for editing a domain")

        self.web.routes.register("/delete/<domain_name>", ["GET"], endpoint=views.delete,
                                 name="view_domain_delete",
                                 context=context.name, description="Deletes a domain")

    def activate_apikey(self):
        views = ApiKeyViews(self)
        prefix_url = "/apikey"
        context = self.web.contexts.register(name="apikey",
                                             template_folder=self._template_folder,
                                             static_folder=self._static_folder,
                                             url_prefix=prefix_url,
                                             description="Context for apikey related objects and actions."
                                             )

        self.web.routes.register("/", ["GET"], endpoint=views.overview, name="view_apikeys",
                                 context=context.name, description="Show all registered apikeys")
        self._user_menu.register("Apikeys", prefix_url)

        self.web.routes.register("/<apikey>", ["GET"], endpoint=views.detail,
                                 name="view_apikey_detail",
                                 context=context.name, description="Shows details of an apikey")

        self.web.routes.register("/add", ["GET", "POST"], endpoint=views.add,
                                 name="view_apikey_add",
                                 context=context.name, description="Shows mask for adding new apikey")

        self.web.routes.register("/delete/<apikey>", ["GET"], endpoint=views.delete,
                                 name="view_apikey_delete",
                                 context=context.name, description="Deletes an apikey")

        self.web.routes.register("/edit/<apikey>", ["GET", "POST"], endpoint=views.edit,
                                 name="view_apikey_edit",
                                 context=context.name, description="Edits an apikey")

    def activate_group(self):
        views = GroupViews(self)
        prefix_url = "/group"
        context = self.web.contexts.register(name="group",
                                             template_folder=self._template_folder,
                                             static_folder=self._static_folder,
                                             url_prefix=prefix_url,
                                             description="Context for group related objects and actions."
                                             )

        self.web.routes.register("/", ["GET"], endpoint=views.overview, name="view_groups",
                                 context=context.name, description="Show all registered groups")
        self._user_menu.register("Groups", prefix_url)

        self.web.routes.register("/<group_name>", ["GET"], endpoint=views.detail,
                                 name="view_group_detail",
                                 context=context.name, description="Shows details of a group")

        self.web.routes.register("/add", ["GET", "POST"], endpoint=views.add,
                                 name="view_group_add",
                                 context=context.name, description="Shows mask for adding a new group")

        self.web.routes.register("/edit/<group_name>", ["GET", "POST"], endpoint=views.edit,
                                 name="view_group_edit",
                                 context=context.name, description="Shows mask for editing a group")

        self.web.routes.register("/delete/<group_name>", ["GET"], endpoint=views.delete,
                                 name="view_group_delete",
                                 context=context.name, description="Deletes a group")

    def activate_permission(self):
        views = PermissionViews(self)
        prefix_url = "/permission"
        context = self.web.contexts.register(name="permission",
                                             template_folder=self._template_folder,
                                             static_folder=self._static_folder,
                                             url_prefix=prefix_url,
                                             description="Context for permission related objects and actions."
                                             )

        self.web.routes.register("/", ["GET"], endpoint=views.overview, name="view_permissions",
                                 context=context.name, description="Show all registered permissions")
        self._user_menu.register("Permissions", prefix_url)

        self.web.routes.register("/<permission_name>", ["GET"], endpoint=views.detail,
                                 name="view_permission_detail",
                                 context=context.name, description="Shows details of a permission")

    def activate_role(self):
        views = RoleViews(self)
        prefix_url = "/role"
        context = self.web.contexts.register(name="role",
                                             template_folder=self._template_folder,
                                             static_folder=self._static_folder,
                                             url_prefix=prefix_url,
                                             description="Context for role related objects and actions."
                                             )

        self.web.routes.register("/", ["GET"], endpoint=views.overview, name="view_roles",
                                 context=context.name, description="Show all registered roles")
        self._user_menu.register("Roles", prefix_url)

        self.web.routes.register("/<role_name>", ["GET"], endpoint=views.detail,
                                 name="view_role_detail",
                                 context=context.name, description="Shows details of a role")

        self.web.routes.register("/add", ["GET", "POST"], endpoint=views.add,
                                 name="view_role_add",
                                 context=context.name, description="Shows mask for adding a new role")

        self.web.routes.register("/edit/<role_name>", ["GET", "POST"], endpoint=views.edit,
                                 name="view_role_edit",
                                 context=context.name, description="Shows mask for editing a role")

        self.web.routes.register("/delete/<role_name>", ["GET"], endpoint=views.delete,
                                 name="view_role_delete",
                                 context=context.name, description="Deletes a role")

    def deactivate(self):
        pass
