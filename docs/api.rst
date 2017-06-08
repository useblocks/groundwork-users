API
===


Plugins
-------

.. _users_web_manager:

GwUsersWebManager
~~~~~~~~~~~~~~~~~

.. autoclass:: groundwork_users.plugins.GwUsersWebManager
   :members:
   :private-members:

Patterns
--------

.. _users_pattern:

GwUsersPattern
~~~~~~~~~~~~~~

Users
+++++

.. autoclass:: groundwork_users.patterns.GwUsersPattern
   :members:
   :private-members:

The following functions are available inside each plugin, which inherits from ``GwUsersPattern`` via
``self.users``.

.. autoclass:: groundwork_users.patterns.gw_users_pattern.users.UsersPlugin
   :members:
   :private-members:
   :undoc-members:

.. autoclass:: groundwork_users.patterns.gw_users_pattern.users.UsersApplication
   :members:
   :private-members:
   :undoc-members:

Errors
^^^^^^
.. autoclass:: groundwork_users.patterns.gw_users_pattern.users.NoUserDatabaseException

.. autoclass:: groundwork_users.patterns.gw_users_pattern.users.NoUserTableException

.. autoclass:: groundwork_users.patterns.gw_users_pattern.users.UserDoesNotExistException



