import os
basedir = os.path.abspath(os.path.dirname(__file__))

# WTF Forms settings
WTF_CSRF_ENABLED = True
SECRET_KEY = '8jOiXeoEVHuv'

# Flask-Oauth settings
FACEBOOK_APP_ID = '832616740148488'
FACEBOOK_APP_SECRET = 'abb48cf90050da6d525ac4d0bc4996af'

# Database settings, using SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Current Map Location
location = {
  'latitude': '28.613939',
  'longitude': '77.209021',
  'placename': 'Delhi'
}

# Pagination
POSTS_PER_PAGE = 2

# Timezone

# Email
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None
ADMIN_EMAILS = ['sarah@thelongtrip.org', 'david@thelongtrip.org']
