from flask import flash, redirect, url_for, request, abort
from flask_babel import _

from groundwork_users.patterns.gw_users_pattern.groups import GroupDoesNotExistException
from groundwork_users.plugins.gw_users_web_manager.forms.group import get_group_form


class GroupViews:
    def __init__(self, plugin):
        self.plugin = plugin

    def add(self):
        """
            Provides a rendered html page for creating a new group.
            :return: Rendered HTML pag (string)
            """
        form = get_group_form(self.plugin)()
        form.users.query = self.plugin.user_model.query.filter()
        form.roles.query = self.plugin.role_model.query.filter()
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

            group_object = self.plugin.groups.register(name=form.name.data,
                                                       description=form.description.data,
                                                       users=form.users.data,
                                                       permissions=permissions_db,
                                                       roles=form.roles.data)

            flash(_("Successfully added group %s" % group_object.name), "info")
            return redirect(url_for('.overview'))

        ret = self.plugin.web.render("group_add.html", form=form)
        return ret

    def overview(self):
        groups = self.plugin.app.groups.get()
        return self.plugin.web.render("group_overview.html", groups=groups)

    def detail(self, group_name):
        group = self.plugin.app.groups.get(group_name)[0]
        return self.plugin.web.render("group_detail.html", group=group)

    def delete(self, group_name):
        try:
            self.plugin.app.groups.delete(group_name)
        except GroupDoesNotExistException:
            self.plugin.log.debug("Group {0} does not exist.".format(group_name))
            abort(404)
        flash(_("Successfully deleted group %s" % group_name), "info")
        return redirect(url_for(".overview"))

    def edit(self, group_name):
        """
        Provides a rendered html page mainly for editing an existing domain.
        :return: Rendered HTML pag (string)
        """
        group = self.plugin.app.groups.get(group_name)[0]

        form = get_group_form(self.plugin)()
        form.users.query = self.plugin.user_model.query.filter()
        form.roles.query = self.plugin.role_model.query.filter()
        form.permissions.choices = [(a.name, a.name) for a in self.plugin.app.permissions.get_from_db()]

        if request.method == 'GET':
            form.name.data = group.name
            form.description.data = group.description
            form.users.data = group.users
            form.permissions.data = [a.name for a in group.permissions]
            form.roles.data = group.roles

        if form.validate_on_submit():
            # For the given permission names we need to find out the permission database objects and set them as
            # the permissions for the user
            permissions_db = []
            for perm in form.permissions.data:
                perm_db = self.plugin.app.permissions.users_db.query(self.plugin.app.permissions.Permission).filter_by(
                    name=perm).first()
                if perm_db is not None:
                    permissions_db.append(perm_db)

            group.name = form.name.data
            group.description = form.description.data
            group.users = form.users.data
            group.permissions = permissions_db
            group.roles = form.roles.data

            self.plugin.users_db.commit()
            flash(_("Successfully edit group %s" % group.name), "info")
            return redirect(url_for('.detail', group_name=group.name))
        return self.plugin.web.render("group_edit.html", form=form, group=group)
