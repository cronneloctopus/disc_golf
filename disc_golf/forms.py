from wtforms import Form, TextField, validators, widgets
from flask.ext.wtf import Form, TextField, BooleanField, IntegerField, \
    SelectField, Required, DateField

BASKETS_CHOICES = [('9', 9), ('18', 18)]


class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class ScoreForm(Form):
    created = DateField('Date', format='%m/%d/%Y')
    score = TextField(validators=[Required()])
    baskets = SelectField(choices=BASKETS_CHOICES)
