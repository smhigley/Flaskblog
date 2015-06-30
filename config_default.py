import os
basedir = os.path.abspath(os.path.dirname(__file__))

# WTF Forms settings
WTF_CSRF_ENABLED = True
SECRET_KEY = ''

# Flask-Oauth settings
FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''

# Database settings, using SQLAlchemy
SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_MIGRATE_REPO = ''

# Current Map Location
location = {
  'latitude': '',
  'longitude': '',
  'placename': ''
}

# Pagination
POSTS_PER_PAGE = 5

# Email
MAIL_SERVER = ''
MAIL_PORT = None
MAIL_USERNAME = None
MAIL_PASSWORD = None
ADMIN_EMAILS = ['']
