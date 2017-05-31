from datetime import datetime


class DomainsPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

    def register(self, name, contact=None, created=None, active=True, users=None):
        return self.app.domains.register(name, contact, created, active, users, plugin=self.plugin)

    def get(self, domain_name=None, **kwargs):
        return self.app.domains.get(domain_name, plugin=self.plugin, **kwargs)

    def delete(self, domain_name):
        return self.app.domains.delete(domain_name, plugin=self.plugin)


class DomainsApplication:
    def __init__(self, app, users_db):
        self.app = app
        self.users_db = users_db

        self.Domain = self.users_db.classes.get("Domain")
        if self.Domain is None:
            raise NoDomainTableException("Database table model 'Domain' not found")

    def register(self, name, contact=None, created=None, active=True, users=None, plugin=None):
        if plugin is None:
            raise ValueError("plugin must not be None")

        if created is None:
            created = datetime.now()

        if users is None:
            users = []

        domain = self.Domain(name=name,
                             contact=contact,
                             created=created,
                             active=active,
                             users=users,
                             plugin_name=plugin.name)
        self.users_db.add(domain)
        self.users_db.commit()
        return domain

    def get(self, domain_name=None, plugin=None, **kwargs):
        if domain_name is not None:
            kwargs["name"] = domain_name

        if plugin is None:
            domains = self.users_db.query(self.Domain).filter_by(**kwargs).all()
        else:
            kwargs["plugin_name"] = plugin.name
            domains = self.users_db.query(self.Domain).filter_by(**kwargs).all()

        return domains

    def delete(self, domain_name, plugin=None):
        domain = self.get(domain_name, plugin=plugin)
        if len(domain) == 0:
            raise DomainDoesNotExistException("Domain {0} does not exist.".format(domain_name))
        domain = domain[0]
        self.users_db.delete(domain)
        self.users_db.commit()
        self.app.log.info("Deleted domain {0}".format(domain.name))


class NoDomainTableException(Exception):
    pass


class DomainDoesNotExistException(Exception):
    pass
