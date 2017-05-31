from flask_babel import _
from flask_security.forms import RegisterForm, Required
from wtforms import StringField, SelectMultipleField, BooleanField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField


def get_user_form(plugin):

    class UserForm(RegisterForm):
        def unique_user(form, field):
            if len(plugin.users.get(field.data)) > 0:
                msg = _('User %s already exists' % field.data)
                raise ValidationError(msg)

        user_name = StringField(
            _('User name'),
            [Required(), unique_user]
        )

        full_name = StringField(
            _('Full name'),
            [Required()]
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
        groups = QuerySelectMultipleField(
            _('Select groups'),
            description="Select groups",
            id="groups",
            get_label="name",
        )

        page = StringField(
            _('Page')
        )
        description = StringField(
            _('Description')
        )
        domain = QuerySelectField(
            _('Domain'),
            # validators=[Required()],
            description="Select domain",
            id="domain",
            get_label="name"
        )

        active = BooleanField(
            _("Active"),
            description="Is user active and can be used for logins?",
            id="active"
        )

    return UserForm
