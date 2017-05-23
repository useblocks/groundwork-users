import json
from flask import render_template, abort, redirect, request, url_for, flash
from flask_wtf import Form
from flask.ext.babel import _
from flask.ext.login import current_user
from wtforms import StringField, TextAreaField, ValidationError, SelectMultipleField
from wtforms.validators import DataRequired
# TODO move this import to groundwork as api
from groundwork.core.plugins.plugin import get_shared_object


class RoleAdd(Form):
    name = StringField(
        _('Role name'),
        validators=[DataRequired()]
    )
    description = TextAreaField(
        _('Role description'),
        validators=[DataRequired()]
    )
    permissions = SelectMultipleField(
        _('Select permissions'),
        description="Select permissions",
        choices=[
            ("", ""),
        ],
    )


# def view_manage_security():
#     """
#     Provides a rendered html page for getting detailed information about a
#     roles.
#     :return: Rendered HTML pag (string)
#     """
#     if not check_permission("manage_roles"):
#         abort(403)
#
#     userStore = get_shared_object("userStore")["shared_object"]
#     users = userStore.get_users()
#     form = RoleAdd()
#
#     if form.validate_on_submit():
#         userStore.find_or_create_role(
#             name=form.name.data, description=form.description.data)
#         userStore.commit()
#         return redirect(url_for('.view_manage_security'))
#
#     rid = request.args.get('rid', None)
#     if rid:
#         userStore.delete_role(rid)
#         userStore.commit()
#         return redirect(url_for('.view_manage_security'))
#
#     ret = render_template("manage_security.html",
#                           roles=userStore.get_all_roles(),
#                           role_form=form, users=users)
#     return ret


def view_roles_overview():
    """
    Provides a rendered html page mainly for getting an overview about all
    roles.
    :return: Rendered HTML pag (string)
    """
    roleStore = get_shared_object("roleStore")["shared_object"]
    roles = roleStore.get_all_roles()
    return render_template("role_overview.html", roles=roles)


def view_roles_details(role_name):
    """
    Provides a rendered html page mainly for getting details about a role.
    :return: Rendered HTML pag (string)
    """
    roleStore = get_shared_object("roleStore")["shared_object"]
    role = roleStore.get_role_by_name(role_name)
    return render_template("role_detail.html", role=role)


def view_roles_edit(role_name):
    """
    Provides a rendered html page mainly for editing details of a role.
    :return: Rendered HTML pag (string)
    """
    roleStore = get_shared_object("roleStore")["shared_object"]
    role = roleStore.get_role_by_name(role_name)
    form = RoleAdd()

    registered_permissions = get_shared_object("Permissions")["shared_object"]
    permission_store = get_shared_object("permissionStore")["shared_object"]
    form.permissions.choices = [(registered_permissions[a]["name"], registered_permissions[a]["name"]) for a in
                                registered_permissions.keys()]

    if request.method == 'GET':
        form.name.data = role.name
        form.description.data = role.description
        form.permissions.data = [a.name for a in role.permissions]

    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data

        # For the given permission names we need to find out the permission database objects and set them as
        # the permissions for the role
        permissions_db = []
        for perm in form.permissions.data:
            permission_object = permission_store.get_permission_by_name(perm)
            if permission_object is None:
                # If the permission is not in the database, we need to create it.
                if registered_permissions[perm]["func"] is None:
                    func_name = None
                else:
                    func_name = registered_permissions[perm]["func"].__name__

                if registered_permissions[perm]["func"] is None:
                    func_params = None
                else:
                    func_params = registered_permissions[perm]["params"]
                permission_object = permission_store.create_permission(name=perm,
                                                                       func_name=func_name,
                                                                       func_params=json.dumps(
                                                                           func_params),
                                                                       plugin_name=registered_permissions[perm][
                                                                           "plugin"])
                permission_store.commit()
            permissions_db.append(permission_object)

        role.permissions = permissions_db
        roleStore.commit()
        flash(_("Successully edited Role"), "info")
        return redirect(url_for('.view_roles_overview'))

    return render_template("role_edit.html", role=role, form=form)


def view_roles_add():
    """
    Provides a rendered html page mainly for adding a new role.
    :return: Rendered HTML pag (string)
    """
    roleStore = get_shared_object("roleStore")["shared_object"]
    form = RoleAdd()

    registered_permissions = get_shared_object("Permissions")["shared_object"]
    permission_store = get_shared_object("permissionStore")["shared_object"]
    form.permissions.choices = [(registered_permissions[a]["name"], registered_permissions[a]["name"]) for a in
                                registered_permissions.keys()]

    if form.validate_on_submit():
        # For the given permission names we need to find out the permission database objects and set them as
        # the permissions for the role
        permissions_db = []
        for perm in form.permissions.data:
            permission_object = permission_store.get_permission_by_name(perm)
            if permission_object is None:
                # If the permission is not in the database, we need to create it.
                if registered_permissions[perm]["func"] is None:
                    func_name = None
                else:
                    func_name = registered_permissions[perm]["func"].__name__

                if registered_permissions[perm]["func"] is None:
                    func_params = None
                else:
                    func_params = registered_permissions[perm]["params"]
                permission_object = permission_store.create_permission(name=perm,
                                                                       func_name=func_name,
                                                                       func_params=json.dumps(
                                                                           func_params),
                                                                       plugin_name=registered_permissions[perm][
                                                                           "plugin"])
                permission_store.commit()
            permissions_db.append(permission_object)

        roleStore.create_role(
            name=form.name.data,
            description=form.description.data,
            permissions=permissions_db
        )
        roleStore.commit()
        flash(_("Successully edited Role"), "info")
        return redirect(url_for('.view_roles_details', role_name=form.name.data))

    return render_template("role_add.html", form=form)


def view_roles_delete(role_name):
    """
    Provides a rendered html page mainly for deleting a role.
    :return: Rendered HTML pag (string)
    """
    roleStore = get_shared_object("roleStore")["shared_object"]
    entry = roleStore.get_role_by_name(role_name)
    if not entry:
        abort(404)

    roleStore.delete(entry)
    roleStore.commit()
    flash(_("Successully deleted Role %s" % entry.name), "info")
    return redirect(url_for(".view_roles_overview"))
