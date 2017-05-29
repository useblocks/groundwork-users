"""
This file contains the database models for the usermanager plugin.

The models may be database specific.  Normally a generic model is used for all
sql related databases.  But for databases like MongoDB and other you will need
special implementations.
"""
from sqlalchemy import Column, ForeignKey, Integer, Table, Text, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from flask_security import UserMixin, RoleMixin


def get_model_classes(db, app):
    Base = db.Base
    metadata = Base.metadata

    # roles_users is needed as linking table between users and roles.
    roles_users = Table(
        'roles_users',
        metadata,
        Column(
            'user_id',
            Integer(),
            ForeignKey('user.id')
        ),
        Column(
            'role_id',
            Integer(),
            ForeignKey('role.id')
        )
    )

    permissions_users = Table(
        'permissions_users',
        metadata,
        Column(
            'user_id',
            Integer(),
            ForeignKey('user.id')
        ),
        Column(
            'permission_id',
            Integer(),
            ForeignKey('permission.id')
        )
    )

    permissions_roles = Table(
        'permissions_roles',
        metadata,
        Column(
            'role_id',
            Integer(),
            ForeignKey('role.id')
        ),
        Column(
            'permission_id',
            Integer(),
            ForeignKey('permission.id')
        )
    )

    groups_users = Table(
        'groups_users',
        metadata,
        Column(
            'user_id',
            Integer(),
            ForeignKey('user.id')
        ),
        Column(
            'group_id',
            Integer(),
            ForeignKey('group.id')
        )
    )

    roles_groups = Table(
        'roles_groups',
        metadata,
        Column(
            'group_id',
            Integer(),
            ForeignKey('group.id')
        ),
        Column(
            'role_id',
            Integer(),
            ForeignKey('role.id')
        )
    )

    permissions_groups = Table(
        'permissions_groups',
        metadata,
        Column(
            'group_id',
            Integer(),
            ForeignKey('group.id')
        ),
        Column(
            'permission_id',
            Integer(),
            ForeignKey('permission.id')
        )
    )

    class Role(Base, RoleMixin):
        """
        Class/Table for storing available roles.
        """
        __tablename__ = "role"
        id = Column(Integer(), primary_key=True)
        name = Column(Text(80), unique=True)
        description = Column(Text(255))
        plugin_name = Column(Text())
        permissions = relationship('Permission', secondary=permissions_roles,
                                   backref=backref('roles', lazy='dynamic'))

    class Permission(Base):
        """
        Class/Table for storing available permissions.
        """
        __tablename__ = "permission"
        id = Column(Integer(), primary_key=True)
        name = Column(Text(255), unique=True)
        description = Column(Text())
        func_name = Column(Text(255))
        func_params = Column(Text())
        plugin_name = Column(Text())

    class Group(Base):
        """
        Class/Table for storing groups.
        """
        __tablename__ = "group"
        id = Column(Integer(), primary_key=True)
        name = Column(Text(255), unique=True)
        description = Column(Text(2048))
        plugin_name = Column(Text())
        users = relationship('User', secondary=groups_users,
                             backref=backref('groups', lazy='dynamic'))
        roles = relationship('Role', secondary=roles_groups,
                             backref=backref('groups', lazy='dynamic'))
        permissions = relationship('Permission', secondary=permissions_groups,
                                   backref=backref('groups', lazy='dynamic'))

    class User(Base, UserMixin):
        """
        Class/Table for storing single users.
        The following columns are needed by the flask-security extension:
        * confirmed_at
        * last_login_at
        * current_login_at
        * last_login_ip
        * current_login_ip
        * login_count
        """
        __tablename__ = "user"
        id = Column(Integer, primary_key=True)
        email = Column(Text(255), unique=True)
        full_name = Column(Text(255))
        password = Column(Text(255))
        user_name = Column(Text(255), unique=True)
        domain = Column(Text(255))
        description = Column(Text(2048))
        page = Column(Text(255))
        plugin_name = Column(Text(255))
        active = Column(Boolean())
        confirmed_at = Column(DateTime())
        last_login_at = Column(DateTime())
        current_login_at = Column(DateTime())
        last_login_ip = Column(Text(255))
        current_login_ip = Column(Text(255))
        login_count = Column(Integer)
        roles = relationship('Role', secondary=roles_users,
                             backref=backref('users', lazy='dynamic'))
        permissions = relationship('Permission', secondary=permissions_users,
                                   backref=backref('users', lazy='dynamic'))
        domain_id = Column(Integer, ForeignKey('domain.id'))
        domain = relationship("Domain", backref="users")

        # ToDo: Reactivate function with new class layout

        def has_permission(self, permission_name, *args, **kwargs):
            """
            Checks, if the user has a given permission (by role or by a direct link to a permission).

            :param permission_name: Name of the permission
            :return: True, if user has permission. Else False.
            """
            # TODO: This should be mapped to permission object, so that "perm in user.permissions" would work
            # TODO: Now we search for a string, which is not so high-performance

            permission_access = False

            # Collect permissions
            #####################
            all_permissions = self.permissions

            # Add role permissions
            for role in self.roles:
                for permission in role.permissions:
                    if permission not in all_permissions:
                        all_permissions.append(permission)

            for group in self.groups:
                # Add direct group permissions
                for permission in group.permissions:
                    if permission not in all_permissions:
                        all_permissions.append(permission)
                # Add group permission given by roles
                for role in group.roles:
                    for permission in role.permissions:
                        if permission not in all_permissions:
                            all_permissions.append(permission)

            # Check permissions
            ###################
            for permission in all_permissions:
                if permission_name == permission.name:
                    permission_access = True
                    break

            if permission_name not in app.permissions._permissions.keys():
                raise PermissionException("Permission %s does not exist" % permission_name)

            if not permission_access:
                return False
            # right now, we only know that the user has the needed permission string.
            # But we need to execute the related permission function, if one was set
            permission = app.permissions._permissions[permission_name]

            # If no extra function for permissions tests is given, the permission check is true
            if permission.func is None:
                return True

            return app.permissions._permissions[permission_name].func(permission_name, *args, **kwargs)

    class Apikey(Base):
        """
        Class/Table for storing api keys
        """
        __tablename__ = "apikey"
        id = Column(Integer(), primary_key=True)
        key = Column(Text(42), unique=True)
        generated = Column(DateTime())
        last_login = Column(DateTime())
        active = Column(Boolean())
        plugin_name = Column(Text())
        user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
        user = relationship('User', backref='apikeys', lazy='joined')

    class Domain(Base):
        """
        Class/Table for storing domains
        """
        __tablename__ = "domain"
        id = Column(Integer(), primary_key=True)
        name = Column(Text(), unique=True)
        contact = Column(Text())
        created = Column(DateTime())
        active = Column(Boolean())
        plugin_name = Column(Text())

    return User, Permission, Role, Apikey, Domain, Group


class PermissionException(Exception):
    pass
