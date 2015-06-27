from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, login_manager, oauth
from .forms import PageForm, PostForm
from .models import User, Post, Page
from config import POSTS_PER_PAGE

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index(page=1):
  user = g.user
  posts = Post.query.paginate(1, 4, False)
  return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/log')
@app.route('/log/<int:page>')
def log(page=1):
  posts = Post.query.paginate(page, POSTS_PER_PAGE, True)
  return render_template('log.html', title='Trip Log', posts=posts)

# Login page
facebook = oauth.remote_app('facebook',
  base_url='https://graph.facebook.com/',
  request_token_url=None,
  access_token_url='/oauth/access_token',
  authorize_url='https://www.facebook.com/dialog/oauth',
  consumer_key=app.config['FACEBOOK_APP_ID'],
  consumer_secret=app.config['FACEBOOK_APP_SECRET'],
  request_token_params={'scope': 'email'}
)

@app.route('/oauth-authorized')
@facebook.authorized_handler
def oauth_authorized(resp):
  next_url = request.args.get('next') or url_for('index')
  if resp is None:
    flash(u'You denied the request to sign in.')
    return redirect(next_url)

  session['oauth_token'] = (resp['access_token'], '')
  fb_user = facebook.get('/me')

  user = User.query.filter_by(social_id=fb_user.data['id']).first()
  if user is None:
    user = User(social_id=fb_user.data['id'], nickname=fb_user.data['name'], email=fb_user.data['email'])
    db.session.add(user)
    db.session.commit()
    # TODO: remove new user functionality, switch to: flash(u'Access Denied. The user %s does not exist.' % fb_user.data['name'])
    return redirect(url_for('index'))

  login_user(user, True) #change this to true when done debugging

  flash('You were signed in as %s' % fb_user.data['name'])
  return redirect(next_url)

@facebook.tokengetter
def get_facebook_oauth_token():
  return session.get('oauth_token')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('index'))

  return facebook.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None, _external=True))

@app.before_request
def before_request():
  g.user = current_user

# Pages
@app.route('/<slug>')
def view_page(slug):
  page = Page.query.filter_by(slug=slug).first()
  if page is None:
    flash('The URL "%s" was not found' % slug)
    return redirect(url_for('index'))
  return render_template('page.html', title=page.title, page=page)

@app.route('/page/new', methods=['GET', 'POST'])
@login_required
def add_page():
  form = PageForm()

  if form.validate_on_submit():
    flash('Page created: %s' % form.title.data)
    page = Page(title=form.title.data, slug=form.slug.data, body=form.body.data)
    db.session.add(page)
    db.session.commit()
    return render_template('page.html', page=page) # TODO: make this a redirect() to avoid reload resubmissions

  return render_template('new_page.html', form=form)

# Posts
@app.route('/log/<slug>')
def view_post(slug):
  post = Post.query.filter_by(slug=slug).first()
  if post is None:
    flash('The URL %s was not found' % slug)
    return redirect(url_for('index'))
  return render_template('post.html', post=post)

@app.route('/log/new', methods=['GET', 'POST'])
@login_required
def add_post():
  form = PostForm()

  if g.user is None or not g.user.is_authenticated():
    return redirect(url_for('login'))

  if form.validate_on_submit():
    flash('Post created: %s' % form.title.data)
    post = Post(title=form.title.data, slug=form.slug.data, body=form.body.data, image=form.image.data, timestamp=datetime.utcnow(), author=g.user)
    db.session.add(post)
    db.session.commit()
    return render_template('post.html', post=post) # TODO: make this a redirect()

  return render_template('new_post.html', form=form)


