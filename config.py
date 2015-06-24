import os
basedir = os.path.abspath(os.path.dirname(__file__))

# WTF Forms settings
WTF_CSRF_ENABLED = True
SECRET_KEY = '8jOiXeoEVHuv'

# OpenID login settings
GOOGLE_CLIENT_ID = '72734181528-l8e5embltfborjh45v67d9f96okkoju9.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'JyHPacRjTreHpV4p0czFN2Gb'
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

# database settings, using SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
