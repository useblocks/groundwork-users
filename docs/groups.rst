.. _groups:

Groups
======

groups are used to bundle users, so that you can assign permissions and roles easily to a group
instead of assigning them separately to each user.

To register, edit or delete groups and their related data, your plugin needs to inherit from GwUsersPattern

Register a new group
--------------------

.. code-block:: python

    from groundwork_users.patterns import GwUsersPattern

    class MyGroupPlugin(GwUsersPattern):
        # Plugin initialisation, no group related stuff here
        def __init__(self, app, *args, **kwargs):
            self.name = "MyGroupPlugin
            super(MyUserPlugin, self).__init__(app, *args, **kwargs)

        def activate(self):
            # Register a new group
            self.groups.register("my_group", "my own group description")

You can also assign users, permission and roles during group registration::

    class MyGroupPlugin(GwUsersPattern):
        ...
         def activate(self):
            # Register a user
            user = self.users.register("test_user", "user@test.com", "my_password")

            # Get a permissions
            permission = self.permissions.get("my_permission")[0]

            # Register a role
            role = self.roles.register("my_role", permissions=[permission])

            # Register a new group
            self.groups.register("my_group", "my own group description",
                                 users=[user],
                                 permissions=[permission],
                                 roles=[role])

Updating an existing group
--------------------------

.. code-block:: python

    class MyGroupPlugin(GwUsersPattern):
        ...

        def change_group(self, group_name):
            group = self.groups.get(group_name)
            if group is None:
                self.log.error("Group {0} does not exist".format(group_name))
            return

            # Make changes on the group model
            group.name = "new_name"

            new_permissions = self.permissions.get("some_new_permissions")
            group.permissions = group.permissions + new_permissions  # Add the new permissions to the existing ones

            # Commit the change
            self.users_db.commit()

Deleting a group
----------------
.. code-block:: python

    class MyGroupPlugin(GwUsersPattern):
        ...
        def deactivate(self):
            self.groups.delete("my_group")

Getting groups
--------------

.. code-block:: python

    class MyGroupPlugin(GwUsersPattern):
        ...

        def activate(self):
            # Get a group by name
            groups = self.groups.get("my_group")
            if groups is not None:
                group = groups[0]

.. note::
    :func:`~groundwork_users.patterns.gw_users_pattern.groups.GroupsPlugin.get` always returns a list, if groups were
    found or None, if no group was found. Even if only a single group is found a list is returned!

You can use additional key-word arguments to filter for groups.
Each given keyword is passed to the sqlalchemy filter function and therefore must be part of the user database model::

    # Filter by plugin_name, which has registered the group
    groups = self.groups.get(plugin_name="MyGroupPlugin")

    # Filter by an user
    users = self.users.get("my_user")
    groups = self.groups.get(users=[users])

Groups database model
---------------------

Below you can see the currently used database model for a group object:

.. literalinclude:: ../groundwork_users/patterns/gw_users_pattern/db/models.py
   :language: ruby
   :lines: 132-146

