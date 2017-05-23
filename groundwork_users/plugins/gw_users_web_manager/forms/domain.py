from flask_babel import _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired


def get_domain_form(plugin):

    def unique_domain(form, field):
        if len(plugin.domains.get(field.data)) > 0:
            msg = _('Domain %s already exists' % field.data)
            raise ValidationError(msg)

    class DomainForm(FlaskForm):
        name = StringField(
            _('Domain name'),
            validators=[DataRequired(), unique_domain]
        )
        contact = TextAreaField(
            _('Domain contact data'),
            validators=[DataRequired()]
        )
        users = QuerySelectMultipleField(
            _('Select Users'),
            description="Select domain users",
            id="users",
            get_label="full_name",
        )

    return DomainForm
