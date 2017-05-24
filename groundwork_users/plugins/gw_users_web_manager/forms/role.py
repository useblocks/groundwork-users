from flask_babel import _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired


def get_role_form(plugin):

    def unique_role(form, field):
        if len(plugin.roles.get(field.data)) > 0:
            msg = _('Role %s already exists' % field.data)
            raise ValidationError(msg)

    class RoleForm(FlaskForm):
        name = StringField(
            _('Role name'),
            validators=[DataRequired(), unique_role]
        )
        description = TextAreaField(
            _('Role description data'),
            validators=[DataRequired()]
        )
        permissions = QuerySelectMultipleField(
            _('Select Permissions'),
            description="Select role permissions",
            id="users",
            get_label="name",
        )
        users = QuerySelectMultipleField(
            _('Select Users'),
            description="Select role users",
            id="users",
            get_label="full_name",
        )

    return RoleForm
