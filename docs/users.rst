.. _users:

Users
=====

To register, edit or delete users and their related data, your plugin needs to inherit from
:class:`~groundwork_users.patterns.GwUsersPattern`


Register a new user
-------------------
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
-----------------------

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
            self.users_db.commit()

Deleting a user
---------------

.. code-block:: python

    class MyUserPlugin(GwUsersPattern):
        ...

        def deactivate(self):
            # Let's delete our test user from database, if the plugin gets deactivated
            self.users.delete("new_user")

Getting users
-------------

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
    users = self.users.get(active = True, roles=roles)



User database model
-------------------

Below you can see the currently used database model for a user object:

.. literalinclude:: ../groundwork_users/patterns/gw_users_pattern/db/models.py
   :language: ruby
   :lines: 148-180

