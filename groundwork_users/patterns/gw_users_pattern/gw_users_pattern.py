from flask_security import Security, SQLAlchemyUserDatastore

from groundwork_database.patterns import GwSqlPattern

from groundwork_users.patterns.gw_users_pattern.db.models import get_model_classes
from groundwork_users.patterns.gw_users_pattern.users import UsersApplication, UsersPlugin
from groundwork_users.patterns.gw_users_pattern.permissions import PermissionsApplication, PermissionsPlugin
from groundwork_users.patterns.gw_users_pattern.roles import RolesApplication, RolesPlugin
from groundwork_users.patterns.gw_users_pattern.apikeys import ApikeysApplication, ApikeysPlugin
from groundwork_users.patterns.gw_users_pattern.domains import DomainsApplication, DomainsPlugin
from groundwork_users.patterns.gw_users_pattern.groups import GroupsApplication, GroupsPlugin


class GwUsersPattern(GwSqlPattern):

    def __init__(self, app, *args, **kwargs):
        db_name = "users_db"
        self.flask_security = None

        try:
            self.needed_plugins.append("GwWeb")
        except AttributeError:
            self.needed_plugins = ["GwWeb"]

        super().__init__(app, *args, **kwargs)

        ###############################################################
        # Database configuration
        ###############################################################
        db_url = app.config.get("USERS_DB_URL", None)
        db_description = "Database for storing users, groups, permissions and other user related data"

        if db_url is None or "":
            raise ValueError("USERS_DB_URL must not be None or empty")
        self.users_db = self.databases.register(db_name, db_url, db_description)
        models = get_model_classes(self.users_db)  # User, Permission, Role, Apikey, Domain, Group

        for model in models:
            self.users_db.classes.register(model)

        self.users_db.create_all()

        ###############################################################
        # Users configuration
        ###############################################################
        # Application context

        if not hasattr(self.app, "users"):
            self.app.users = UsersApplication(self.app)

        if not hasattr(self.app, "permissions"):
            self.app.permissions = PermissionsApplication(app, self.users_db)

        if not hasattr(self.app, "roles"):
            self.app.roles = RolesApplication(app, self.users_db)

        if not hasattr(self.app, "apikeys"):
            self.app.apikeys = ApikeysApplication(app, self.users_db)

        if not hasattr(self.app, "domains"):
            self.app.domains = DomainsApplication(app, self.users_db)

        if not hasattr(self.app, "groups"):
            self.app.groups = GroupsApplication(app, self.users_db)

        # Plugin context

        #: Instance of :class:`~.UsersPlugin`.
        #: Provides functions to register and manage users
        self.users = UsersPlugin(self)
        self.permissions = PermissionsPlugin(self)
        self.roles = RolesPlugin(self)
        self.apikeys = ApikeysPlugin(self)
        self.domains = DomainsPlugin(self)
        self.groups = GroupsPlugin(self)

        # Create a signal to configure flask-security after plugin activation.
        self.signals.connect(receiver="",
                             signal="plugin_activate_post",
                             function=self.configure_web_security,
                             description="Cares about the correct configuration of flask security for GwUsers",
                             sender=self)

    def configure_web_security(self, plugin, *args, **kwargs):
        # Flask-Security configuration
        User = self.users_db.classes.get("User")
        Role = self.users_db.classes.get("Role")
        user_datastore = SQLAlchemyUserDatastore(self.users_db, User, Role)
        self.flask_security = Security(self.app.web.flask, user_datastore)

