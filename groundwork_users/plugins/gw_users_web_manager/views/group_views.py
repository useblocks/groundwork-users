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

        if form.validate_on_submit():
            group_object = self.plugin.groups.register(name=form.name.data,
                                                       description=form.description.data,
                                                       users=form.users.data)

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

        if request.method == 'GET':
            form.name.data = group.name
            form.description.data = group.description
            form.users.data = group.users

        if form.validate_on_submit():
            group.name = form.name.data
            group.description = form.description.data
            group.users = form.users.data

            self.plugin.users_db.commit()
            flash(_("Successfully edit group %s" % group.name), "info")
            return redirect(url_for('.detail', group_name=group.name))
        return self.plugin.web.render("group_edit.html", form=form, group=group)
