from flask_babel import _
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired


def get_apikey_form(plugin):

    def unique_apikey(form, field):
        if len(plugin.apikeys.get(field.data)) > 0:
            msg = _('Apikey %s already exists' % field.data)
            raise ValidationError(msg)

    class ApikeyForm(FlaskForm):
        key = StringField(
            _('API key'),
            validators=[DataRequired(), unique_apikey],
            render_kw={'readonly': True}
        )
        active = BooleanField(
            _("Active"),
            description="Is user active and can be used for logins?",
            id="active"
        )

        user = QuerySelectField(
            _('Select User'),
            description="Select api key user",
            id="user",
            get_label="full_name",
        )

    return ApikeyForm
