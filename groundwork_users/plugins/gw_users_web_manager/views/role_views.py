from flask import flash, redirect, url_for, request, abort
from flask_babel import _

from groundwork_users.patterns.gw_users_pattern.roles import RoleDoesNotExistException
from groundwork_users.plugins.gw_users_web_manager.forms.role import get_role_form


class RoleViews:
    def __init__(self, plugin):
        self.plugin = plugin

    def add(self):
        """
            Provides a rendered html page for creating a new user.
            :return: Rendered HTML pag (string)
            """
        form = get_role_form(self.plugin)()
        form.users.query = self.plugin.user_model.query.filter()
        form.permissions.query = self.plugin.permission_model.query.filter()

        if form.validate_on_submit():
            role_object = self.plugin.roles.register(name=form.name.data,
                                                     description=form.description.data,
                                                     permissions=form.permissions.data,
                                                     users=form.users.data)

            self.plugin.users_db.commit()
            flash(_("Successfully added role %s" % role_object.name), "info")
            return redirect(url_for('.overview'))

        ret = self.plugin.web.render("role_add.html", form=form)
        return ret

    def overview(self):
        roles = self.plugin.app.roles.get()
        return self.plugin.web.render("role_overview.html", roles=roles)

    def detail(self, role_name):
        try:
            role = self.plugin.app.roles.get(role_name)[0]
        except IndexError:
            abort(404)
        return self.plugin.web.render("role_detail.html", role=role)

    def delete(self, role_name):
        try:
            self.plugin.app.roles.delete(role_name)
        except RoleDoesNotExistException:
            self.plugin.log.debug("Role {0} does not exist.".format(role_name))
            abort(404)
        flash(_("Successfully deleted role %s" % role_name), "info")
        return redirect(url_for(".overview"))

    def edit(self, role_name):
        """
        Provides a rendered html page mainly for editing an existing role.
        :return: Rendered HTML pag (string)
        """
        role = self.plugin.app.roles.get(role_name)[0]

        form = get_role_form(self.plugin)()
        form.users.query = self.plugin.user_model.query.filter()
        form.permissions.query = self.plugin.permission_model.query.filter()

        form.name.validators = []

        if request.method == 'GET':
            form.name.data = role.name
            form.description.data = role.description
            form.users.data = role.users
            form.permissions.data = role.permissions

        if form.validate_on_submit():
            role.name = form.name.data
            role.description = form.description.data
            role.users = form.users.data
            role.permissions = form.permissions.data

            self.plugin.users_db.commit()
            flash(_("Successfully edit role %s" % role.name), "info")
            return redirect(url_for('.detail', role_name=role.name))
        return self.plugin.web.render("role_edit.html", form=form, role=role)
