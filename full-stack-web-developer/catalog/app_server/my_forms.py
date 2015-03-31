from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Optional

""" Login form """
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

""" category form """
class CategoryForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])

""" Item form """
class ItemForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(max=1000)])
    category = IntegerField('category', validators=[DataRequired()])

""" Generic form holding optional values """
class OptionalForm(Form):
    optional = StringField('optional', validators=[Optional()])
