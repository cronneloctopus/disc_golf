from wtforms import Form, TextField, validators
from flask.ext.wtf import Form, TextField, BooleanField, IntegerField, \
    SelectField, Required

BASKETS_CHOICES = [('9', 9), ('18', 18)]


class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class ScoreForm(Form):
    score = TextField(validators=[Required()])
    baskets = SelectField(choices=BASKETS_CHOICES)
