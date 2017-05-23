from flask import flash, redirect, url_for, request, abort
from flask_babel import _

from groundwork_users.patterns.gw_users_pattern.domains import DomainDoesNotExistException
from groundwork_users.plugins.gw_users_web_manager.forms.domain import get_domain_form


class DomainViews:
    def __init__(self, plugin):
        self.plugin = plugin

    def add(self):
        """
            Provides a rendered html page for creating a new user.
            :return: Rendered HTML pag (string)
            """
        form = get_domain_form(self.plugin)()
        form.users.query = self.plugin.user_model.query.filter()

        if form.validate_on_submit():
            domain_object = self.plugin.domains.register(name=form.name.data,
                                                         contact=form.contact.data,
                                                         users=form.users.data)

            self.plugin.users_db.commit()
            flash(_("Successfully added domain %s" % domain_object.name), "info")
            return redirect(url_for('.overview'))

        ret = self.plugin.web.render("domain_add.html", form=form)
        return ret

    def overview(self):
        domains = self.plugin.app.domains.get()
        return self.plugin.web.render("domain_overview.html", domains=domains)

    def detail(self, domain_name):
        domain = self.plugin.app.domains.get(domain_name)[0]
        return self.plugin.web.render("domain_detail.html", domain=domain)

    def delete(self, domain_name):
        try:
            self.plugin.app.domains.delete(domain_name)
        except DomainDoesNotExistException:
            self.plugin.log.debug("Domain {0} does not exist.".format(domain_name))
            abort(404)
        flash(_("Successfully deleted domain %s" % domain_name), "info")
        return redirect(url_for(".overview"))

    def edit(self, domain_name):
        """
        Provides a rendered html page mainly for editing an existing domain.
        :return: Rendered HTML pag (string)
        """
        domain = self.plugin.app.domains.get(domain_name)[0]

        form = get_domain_form(self.plugin)()
        form.users.query = self.plugin.user_model.query.filter()

        if request.method == 'GET':
            form.name.data = domain.name
            form.contact.data = domain.contact
            form.users.data = domain.users

        if form.validate_on_submit():
            domain.name = form.name.data
            domain.contact = form.contact.data
            domain.users = form.users.data

            self.plugin.users_db.commit()
            flash(_("Successfully edit domain %s" % domain.name), "info")
            return redirect(url_for('.detail', domain_name=domain.name))
        return self.plugin.web.render("domain_edit.html", form=form, domain=domain)
