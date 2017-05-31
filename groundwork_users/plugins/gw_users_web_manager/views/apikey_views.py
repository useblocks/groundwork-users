import uuid
from flask import redirect, url_for, flash, request, abort
from flask_babel import _

from groundwork_users.patterns.gw_users_pattern.apikeys import ApikeyDoesNotExistException
from groundwork_users.plugins.gw_users_web_manager.forms.apikey import get_apikey_form


class ApiKeyViews():
    def __init__(self, plugin):
        self.plugin = plugin

    def add(self):
        """
            Provides a rendered html page for creating a new apikey.
            :return: Rendered HTML pag (string)
            """
        form = get_apikey_form(self.plugin)()
        form.user.query = self.plugin.user_model.query.filter()
        form.key.data = str(uuid.uuid4())

        if form.validate_on_submit():
            apikey_object = self.plugin.apikeys.register(key=form.key.data,
                                                         active=form.active.data,
                                                         user=form.user.data)

            self.plugin.users_db.commit()
            flash(_("Successfully added apikey %s" % apikey_object.key), "info")
            return redirect(url_for('.overview'))

        ret = self.plugin.web.render("apikey_add.html", form=form)
        return ret

    def overview(self):
        apikeys = self.plugin.app.apikeys.get()
        return self.plugin.web.render("apikey_overview.html", apikeys=apikeys)

    def detail(self, apikey):
        try:
            apikey = self.plugin.app.apikeys.get(apikey)[0]
            return self.plugin.web.render("apikey_detail.html", apikey=apikey)
        except IndexError:
            self.plugin.log.debug("Apikey does not exist: {0}".format(apikey))
            abort(404)
        except Exception:
            self.plugin.log.warning("Apikey deletion hasn't  worked: {0}".format(apikey))
            abort(500)

    def delete(self, apikey):
        try:
            self.plugin.app.apikeys.delete(apikey)
        except ApikeyDoesNotExistException:
            abort(404)

        flash(_("Successfully deleted API key %s" % apikey), "info")
        return redirect(url_for(".overview"))

    def edit(self, apikey):
        """
            Provides a rendered html page for editing a new apikey.
            :return: Rendered HTML pag (string)
            """
        try:
            apikey = self.plugin.app.apikeys.get(apikey)[0]
        except IndexError:
            self.plugin.log.debug("Apikey does not exist: {0}".format(apikey))
            abort(404)

        form = get_apikey_form(self.plugin)()
        form.user.query = self.plugin.user_model.query.filter()
        form.key.data = str(uuid.uuid4())

        if request.method == 'GET':
            form.key.data = apikey.key
            form.active.data = apikey.active
            form.user.data = apikey.user

        if form.validate_on_submit():
            apikey.key = form.key.data
            apikey.active = form.active.data
            apikey.user = form.user.data

            self.plugin.users_db.commit()
            flash(_("Successfully edited apikey %s" % apikey.key), "info")
            return redirect(url_for('.overview'))

        ret = self.plugin.web.render("apikey_edit.html", form=form)
        return ret
