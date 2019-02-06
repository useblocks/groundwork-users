Configuration
=============

Application configuration parameters
------------------------------------

USERS_DB_URL
~~~~~~~~~~~~

Database connection string / url, which defines the database to use for storing user related data.::

    USERS_DB_URL = "sqlite:///{0}/my_users.db".format(APP_PATH)

