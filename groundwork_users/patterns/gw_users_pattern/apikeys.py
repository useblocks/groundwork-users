from datetime import datetime
import uuid


class ApikeysPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

    def register(self, key=None, generated=None, last_login=None, active=True, user=None):
        return self.app.apikeys.register(key, generated, last_login, active, user, plugin=self.plugin)

    def get(self, key=None, **kwargs):
        return self.app.apikeys.get(key, plugin=self.plugin, **kwargs)

    def delete(self, key):
        return self.app.apikeys.delete(key, plugin=self.plugin)


class ApikeysApplication:
    def __init__(self, app, users_db):
        self.app = app
        self.users_db = users_db

        self.Apikey = self.users_db.classes.get("Apikey")
        if self.Apikey is None:
            raise NoApikeyTableException("Database table model 'Apikey' not found")

    def register(self, key=None, generated=None, last_login=None, active=True, user=None, plugin=None):
        if plugin is None:
            raise ValueError("plugin must not be None")

        if key is None:
            key = str(uuid.uuid4())

        if generated is None:
            generated = datetime.now()
        apikey = self.Apikey(key=key,
                             generated=generated,
                             last_login=last_login,
                             active=active,
                             user=user,
                             plugin_name=plugin.name)
        self.users_db.add(apikey)
        self.users_db.commit()
        return apikey

    def get(self, key=None, plugin=None, **kwargs):
        if key is not None:
            kwargs["key"] = key

        if plugin is None:
            apikeys = self.users_db.query(self.Apikey).filter_by(**kwargs).all()
        else:
            kwargs["plugin_name"] = plugin.name
            apikeys = self.users_db.query(self.Apikey).filter_by(**kwargs).all()

        return apikeys

    def delete(self, key, plugin=None):
        apikey = self.get(key, plugin=plugin)
        if len(apikey) == 0:
            raise ApikeyDoesNotExistException("Apikey {0} does not exist.".format(key))
        apikey = apikey[0]
        self.users_db.delete(apikey)
        self.users_db.commit()
        self.app.log.info("Deleted apikey {0}".format(apikey.key))


class NoApikeyTableException(Exception):
    pass


class ApikeyDoesNotExistException(Exception):
    pass
