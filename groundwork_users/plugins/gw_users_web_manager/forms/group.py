from flask_babel import _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired


def get_group_form(plugin):

    def unique_group(form, field):
        if len(plugin.groups.get(field.data)) > 0:
            msg = _('Group %s already exists' % field.data)
            raise ValidationError(msg)

    class GroupForm(FlaskForm):
        name = StringField(
            _('Group name'),
            validators=[DataRequired(), unique_group]
        )
        description = TextAreaField(
            _('Description')
        )
        users = QuerySelectMultipleField(
            _('Members'),
            description="Select group members",
            id="users",
            get_label="full_name",
        )
        roles = QuerySelectMultipleField(
            _('Select roles'),
            description="Select permission roles",
            id="roles",
            get_label="name",
        )
        permissions = SelectMultipleField(
            _('Select permissions'),
            description="Select permissions",
            choices=[("", "")],
        )

    return GroupForm
