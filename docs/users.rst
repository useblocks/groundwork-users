Users
=====

Using users API
---------------

To register, edit or delete users and their related data, your plugin needs to inherit from
:class:`~groundwork_users.patterns.GwUsersPattern`


Register a new user
~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    from groundwork_users.patterns import GwUsersPattern

    class MyUserPlugin(GwUsersPattern):
        # Plugin initialisation, no user related stuff here
        def __init__(self, app, *args, **kwargs):
            self.name = "MyUserPlugin
            super(MyUserPlugin, self).__init__(app, *args, **kwargs)

        def activate(self):
            # Register a new user
            user = self.users.register("test_user", "user@test.com", "my_password")

If you already have registered some :ref:`permissions`, :ref:`roles`, :ref:`groups` or :ref:`domains`
you can use them during the registration process::

    class MyUserPlugin(GwUsersPattern):
        ...

        def activate(self, ):
            user_roles = self.roles.get("my_role")
            user_permissions = self.permission.get("my_permission")
            user_groups = self.roles.get("my_group")
            user_domain = self.domains.get("my_domain")

            user = self.users.register(user_name="new_user",
                                       full_name="New User",
                                       email="new@user.com",
                                       password="secret_password",
                                       page="htttp://user_page.com",
                                       description="My new user for tests",
                                       domain=users_domain,
                                       groups=user_groups,
                                       roles=user_roles,
                                       permissions=user_permissions
                                       )

Update an existing user
~~~~~~~~~~~~~~~~~~~~~~~

To update an existing user you can use the Users database model and commit the change to the database
after changes has been made::


    class MyUserPlugin(GwUsersPattern):
        ...

        def change_user(self, user_name):
            user = self.users.get(user_name)
            if user is None:
                self.log.error("User {0} does not exist".format(user_name))
                return

            # Make a change on the user model
            user.full_name = "My new user name"

            # Commit the change
            self.users.users_db.commit()

Deleting a user
~~~~~~~~~~~~~~~

.. code-block:: python

    class MyUserPlugin(GwUsersPattern):
        ...

        def deactivate(self):
            # Let's delete our test user from database, if the plugin gets deactivated
            self.users.delete("new_user")

Getting users
~~~~~~~~~~~~~

For searching and filter users you can use the :func:`~groundwork_users.patterns.gw_users_pattern.users.UsersPlugin.get`
function::

    class MyUserPlugin(GwUsersPattern):
        ...

        def activate(self):
            # Get a user by user_name
            users = self.users.get("new_user")
            if users is not None:
                user = users[0]

.. note::
    :func:`~groundwork_users.patterns.gw_users_pattern.users.UsersPlugin.get` always returns a list, if users were
    found or None, if no user was found. Even if only a single user is found a list is returned!

You can use additional key-word arguments to filter for users.
Each given keyword is passed to the sqlalchemy filter function and therefore must be part of the user database model::

    # Filter by full name
    users = self.users.get(full_name="user")

    # Filter by active status
    users = self.users.get(active = True)

    # Filter my multiple values
    roles = self.roles.get("my_role")
    users = self.users.get(active = True, roles=role)

Using users web views
---------------------

By using the plugin :class:`~groundwork_users.plugins.GwUsersWebManager` you get automatically web views and menu entries
to view, create, edit and delete users and their related objects.

All you have to do is to load and activate :class:`~groundwork_users.plugins.GwUsersWebManager`::

    from groundwork import App

    def start_app():
        app = App(["my_config_file"])
        app.plugins.activate(["GwUsersWebManager", "Another_Plugin", "One_More_Plugin"])

        # Register a new user on application level
        user = app.users.register("test_user", "user@test.com", "my_password")

    if "main" in __name__:
        start-app()

After starting your application, you should be able to see a list of users under the url **http://your_server/user**

.. thumbnail:: _images/web_user_list.png
   :width: 80%
   :align: center

   List of all registered users

Handling users
~~~~~~~~~~~~~~

Before you can start creating and editing users, you have to be sure the current_user has the right permission to
perform these actions.

:class:`~groundwork_users.plugins.GwUsersWebManager` creates some permission during activations and secures the
related views and buttons::

* user_view_all
* user_edit_all
* user_delete_all
* user_view_own
* user_edit_own
* user_delete_own

**xx_all** allows to perform the action on **all** user objects.

**xx_own** allows the currently logged in user to perform the related action on its own user profile only.

So to finally create a user via web-interface, you already need an existing user with the right permissions.

But that's quite easy to achieve, by creating some sort of an "administrator" user during application start up::

    from groundwork import App

    def start_app():
        app = App(["my_config_file"])
        app.plugins.activate(["GwUsersWebManager", "Another_Plugin", "One_More_Plugin"])

        # Check if an "admin" user already exists
        admin_user = app.users.get("admin")
        if admin_user is None or len(admin_user) == 0:
            # Get all existing permissions because our new user is admin. Muhaaaa!
            admin_permissions = app.permission.get()

            # Register admin user
            admin_user = app.users.register("admin", "admin@my_company.com", "admin_password",
                                            permissions=admin_permissions)

    if "main" in __name__:
        start-app()

After you started your application you can login with the admin user and have all available permissions to perform
really every action.

User database model
-------------------

Below you can see the currently used database model for a user object:

.. literalinclude:: ../groundwork_users/patterns/gw_users_pattern/db/models.py
   :language: ruby
   :lines: 148-180

