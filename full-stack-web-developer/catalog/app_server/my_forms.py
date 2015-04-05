from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Optional

class LoginForm(Form):
    """
    Form to login an user using OpenID
    """
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class CategoryForm(Form):
    """
    Form to Add & Edit a category
    """
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])


class ItemForm(Form):
    """
    Form to Add & Edit an Item
    """
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(max=1000)])
    category = IntegerField('category', validators=[DataRequired()])


class OptionalForm(Form):
    """
    A Generic form where a field is optional.
    Used for Deleting Category and Item
    """
    optional = StringField('optional', validators=[Optional()])
