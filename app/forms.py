from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, RadioField, validators
from config import POST_CATEGORIES
# from flask.ext.pagedown.fields import PageDownField

class PageForm(Form):
  title = StringField('title', validators=[validators.DataRequired()])
  slug = StringField('slug', validators=[validators.DataRequired(), validators.Regexp('[\w-]+$', message="The slug must contain only letters, numbers, and dashes")])
  # body = PageDownField('body', validators=[validators.DataRequired()])
  body = TextAreaField('body', validators=[validators.DataRequired()])

class PostForm(Form):
  title = StringField('title', validators=[validators.DataRequired()])
  slug = StringField('slug', validators=[validators.DataRequired(), validators.Regexp('[\w-]+$', message="The slug must contain only letters, numbers, and dashes")])
  location = StringField('location')
  # categories = RadioField('category', choices=POST_CATEGORIES)
  # body = PageDownField('body', validators=[validators.DataRequired()])
  body = TextAreaField('body', validators=[validators.DataRequired()])
  image = StringField('image')

class ContactForm(Form):
  name = StringField('name', validators=[validators.DataRequired()])
  email = StringField('email', validators=[validators.DataRequired(), validators.Email()])
  message = TextAreaField('message', validators=[validators.DataRequired()])