from setuptools import setup

setup(
  name='TheLongTrip',
  version='1.0',
  description='A travel blog made with Flask and hope',
  long_description=__doc__,
  url='git@github.com:smhigley/Flaskblog.git',
  author='Sarah Higley'
  zip_safe=False,
  install_requires=[
    'Flask==0.10.1',
    'Flask-Login==0.2.11',
    'Flask-OAuth==0.12',
    'Flask-Mail==0.9.1',
    'Flask-SQLAlchemy==2.0',
    'sqlalchemy-migrate==0.9.2',
    'Flask-WTF==0.10.3',
    'Flask-PageDown==0.2.1',
    'Flask-WhooshAlchemy==0.56',
    'Flask-Babel==0.9',
    'guess-language==0.2',
    'flipflop==1.0',
    'coverage==3.7.1'
  ]
)