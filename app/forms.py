from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
  openid = StringField('openid', validators=[DataRequired()])
  remember_me = BooleanField('remember_me', default=False)

class PageForm(Form):
  title = StringField('title', validators=[DataRequired()])
  slug = StringField('slug', validators=[DataRequired()]) # TODO: add better validation to this: no spaces, capitals, special chars
  body = StringField('body', validators=[DataRequired()])

class PostForm(Form):
  title = StringField('title', validators=[DataRequired()])
  slug = StringField('slug', validators=[DataRequired()]) # TODO: add better validation to this: no spaces, capitals, special chars
  body = StringField('body', validators=[DataRequired()])
  image = StringField('image')