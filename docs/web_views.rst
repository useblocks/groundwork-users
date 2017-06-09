Web views
=========

Using web views
---------------

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

Set permisisons
---------------

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