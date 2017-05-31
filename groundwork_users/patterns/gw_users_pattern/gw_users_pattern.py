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

        super(GwUsersPattern, self).__init__(app, *args, **kwargs)

        ###############################################################
        # Database configuration
        ###############################################################
        db_url = app.config.get("USERS_DB_URL", None)
        db_description = "Database for storing users, groups, permissions and other user related data"

        if db_url is None or "":
            raise ValueError("USERS_DB_URL must not be None or empty")
        self.users_db = self.databases.register(db_name, db_url, db_description)
        models = get_model_classes(self.users_db, self.app)  # User, Permission, Role, Apikey, Domain, Group

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

        self.anonymous_name = "anonymous"
        self.anonymous_role = None
        self.anonymous_user = None

    def configure_web_security(self, plugin, *args, **kwargs):
        # Flask-Security configuration
        User = self.users_db.classes.get("User")
        Role = self.users_db.classes.get("Role")
        user_datastore = SQLAlchemyUserDatastore(self.users_db, User, Role)

        # The following configuration is needed to provide the flask-security
        # extension the correct location of our custom templates for login,
        # password reset, ...
        self.app.web.flask.config[
            "SECURITY_FORGOT_PASSWORD_TEMPLATE"] = "forms/forgot_password.html"
        self.app.web.flask.config[
            "SECURITY_LOGIN_USER_TEMPLATE"] = "forms/login_user.html"
        self.app.web.flask.config[
            "SECURITY_REGISTER_USER_TEMPLATE"] = "forms/register_user.html"
        self.app.web.flask.config[
            "SECURITY_RESET_PASSWORD_TEMPLATE"] = "forms/reset_password.html"
        self.app.web.flask.config[
            "SECURITY_SEND_CONFIRMATION_TEMPLATE"] = "forms/send_confirmation.html"

        # Specify the correct urls for login, register, ...
        self.app.web.flask.config["SECURITY_LOGIN_URL"] = "/login"
        self.app.web.flask.config["SECURITY_LOGOUT_URL"] = "/logout"
        self.app.web.flask.config[
            "SECURITY_REGISTER_URL"] = "/register"

        # Activate the needed flask-security features by setting the correct
        # flags
        self.app.web.flask.config["SECURITY_TRACKABLE"] = True

        self.anonymous_role = self.roles.register("Anonymous", "special role for anonymous accounts")
        self.anonymous_user = self.users.register("anonymous", "none@email.com", "",
                                                  full_name="Anonymous", roles=[self.anonymous_role])

        class AnonymousUser(User):
            """
            Anonymous user class for flask security/login.
            Security extension initiates this class by itself during start up.
            So every parameter we set here will become fix during runtime.
            This means, we can not reconfigure the anonymous user.
            So every permission the user gets, must be already set in db during start up.
            --> Restart app, if you changed anonymous permissions in DB!
            """
            # TODO: Using self inside this class def is really ugly. self means here the plugin class, not
            # TODO: the anonymous user class.
            flask = self.web.flask
            is_authenticated = False
            is_anonymous = True
            anonymous_name = self.anonymous_name
            anonymous_user = self.users.get(anonymous_name)

            # def __init__(self):
            #     if self.anonymous_name is not None:
            #         with self.flask.app_context():
            #             self.anonymous = self.users.get("anonymous")
            #             if self.anonymous is not None:
            #                 self.permissions = self.anonymous.permissions

        self.flask_security = Security(self.app.web.flask, user_datastore, anonymous_user=AnonymousUser)
