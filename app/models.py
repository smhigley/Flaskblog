from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  social_id = db.Column(db.Integer, index=True, unique=True)
  nickname = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), unique=True)
  posts = db.relationship('Post', backref='author', lazy='dynamic')

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    try:
      return unicode(self.id)  # python 2
    except NameError:
      return str(self.id)  # python 3

  def __repr__(self):
    return '<User %r>' % (self.nickname)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64))
  slug = db.Column(db.String(32))
  body = db.Column(db.String(140))
  image = db.Column(db.String(64))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Post %r>' % (self.title)

  def get_thumbnail(self):
    extension = self.image.rfind('.')
    thumb = self.image[:extension] + '_thumb' + self.image[extension:]
    return thumb


class Page(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64))
  slug = db.Column(db.String(32))
  body = db.Column(db.String(140))

  def __repr__(self):
    return '<Page %r>' % (self.title)