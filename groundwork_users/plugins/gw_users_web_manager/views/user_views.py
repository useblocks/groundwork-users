from flask import flash, redirect, url_for, request, abort

try:
    from flask_babel import _
except ImportError:
    from flask.ext.babel import _

from flask_security.utils import encrypt_password

from groundwork_users.patterns.gw_users_pattern.users import UserDoesNotExistException
from groundwork_users.plugins.gw_users_web_manager.forms.user import get_user_form


class UserViews:
    def __init__(self, plugin):
        self.plugin = plugin

    def add(self):
        """
            Provides a rendered html page for creating a new user.
            :return: Rendered HTML pag (string)
            """
        form = get_user_form(self.plugin)()
        form.roles.query = self.plugin.role_model.query.filter()
        form.domain.query = self.plugin.domain_model.query.filter()
        form.groups.query = self.plugin.group_model.query.filter()

        form.permissions.choices = [(a.name, a.name) for a in self.plugin.app.permissions.get_from_db()]

        if form.validate_on_submit():
            # For the given permission names we need to find out the permission database objects and set them as
            # the permissions for the user
            permissions_db = []
            for perm in form.permissions.data:
                perm_db = self.plugin.app.permissions.users_db.query(self.plugin.app.permissions.Permission).filter_by(
                    name=perm).first()
                if perm_db is not None:
                    permissions_db.append(perm_db)

            self.plugin.users.register(user_name=form.user_name.data,
                                       password=form.password.data,
                                       full_name=form.full_name.data,
                                       email=form.email.data,
                                       page=form.page.data,
                                       description=form.description.data,
                                       domain=form.domain.data,
                                       groups=form.groups.data,
                                       roles=form.roles.data,
                                       permissions=permissions_db,
                                       confirmed_at=None,
                                       active=form.active.data)
            self.plugin.users_db.commit()
            flash(_("Successfully created User"), "info")
            return redirect(url_for('.overview'))

        ret = self.plugin.web.render("usermanager_add.html", form=form)
        return ret

    def overview(self):
        users = self.plugin.app.users.get()
        return self.plugin.web.render("usermanager_overview.html", users=users)

    def detail(self, user_name):
        user = self.plugin.app.users.get(user_name)[0]
        return self.plugin.web.render("usermanager_detail.html", user=user)

    def edit(self, user_name):
        """
        Provides a rendered html page for creating a new user.
        :return: Rendered HTML pag (string)
        """
        user = self.plugin.app.users.get(user_name)[0]

        form = get_user_form(self.plugin)()
        form.roles.query = self.plugin.role_model.query.filter()
        form.domain.query = self.plugin.domain_model.query.filter()
        form.groups.query = self.plugin.group_model.query.filter()

        form.permissions.choices = [(a.name, a.name) for a in self.plugin.app.permissions.get_from_db()]

        # XXX email, user are readonly
        form.email.validators = []
        form.user_name.validators = []
        form.password.validators = []

        if request.method == "GET":
            form.user_name.data = user.user_name
            form.full_name.data = user.full_name
            form.email.data = user.email
            form.page.data = user.page
            form.description.data = user.description
            form.domain.data = user.domain
            form.groups.data = user.groups
            form.roles.data = user.roles
            form.permissions.data = [a.name for a in user.permissions]
            form.active.data = user.active

        if form.validate_on_submit():
            # For the given permission names we need to find out the permission database objects and set them as
            # the permissions for the user
            permissions_db = []
            for perm in form.permissions.data:
                perm_db = self.plugin.app.permissions.users_db.query(self.plugin.app.permissions.Permission).filter_by(
                    name=perm).first()
                if perm_db is not None:
                    permissions_db.append(perm_db)
                # permissions_db.append(self.plugin.app.permissions.get(perm))
            user.permissions = permissions_db

            if form.password.data:
                user.password = encrypt_password(form.password.data)

            user.full_name = form.full_name.data
            user.page = form.page.data
            user.description = form.description.data
            user.domain = form.domain.data
            user.groups = form.groups.data
            user.roles = form.roles.data
            user.permissions = permissions_db
            user.active = form.active.data

            self.plugin.users_db.commit()
            flash(_("Successfully edited User %s" % user.full_name), "info")
            return redirect(url_for('.detail', user_name=user.user_name))

        ret = self.plugin.web.render("usermanager_edit.html", form=form, user=user)
        return ret

    def delete(self, user_name):
        try:
            self.plugin.app.users.delete(user_name)
        except UserDoesNotExistException:
            self.plugin.log.debug("User {0} does not exist".format(user_name))
            abort(404)

        flash(_("Successfully deleted user %s" % user_name), "info")
        return redirect(url_for(".overview"))
