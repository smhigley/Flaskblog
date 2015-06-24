from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from app import app, db, login_manager, oid
from .forms import LoginForm, PageForm, PostForm
from .models import User, Post, Page

@login_manager.user_loader
def load_user(id):
  return User.get(int(id))

@app.route('/')
@app.route('/index')
def index():
  user = g.user
  posts = [  # fake array of posts
    { 
      'author': {'nickname': 'John'}, 
      'body': 'Beautiful day in Portland!' 
    },
    { 
      'author': {'nickname': 'Susan'}, 
      'body': 'The Avengers movie was so cool!' 
    }
  ]
  return render_template('index.html', title='Home', user=user, posts=posts)

# Login page
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('index'))

  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    return oid.try_login(form.openid.data, ask_for=['email', 'nickname'], ask_for_optional=['fullname'])

  return render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])

@app.before_request
def before_request():
  g.user = current_user

@oid.after_login
def after_login(resp):
  if resp.email is None or resp.email == "":
    flash('Invalid login. Please try again.')
    return redirect(url_for('login'))

  user = User.query.filter_by(email=resp.email).first()
  if user is None:
    nickname = resp.nickname
    if nickname is None or nickname == "":
      nickname = resp.email.split('@')[0]
    user = User(nickname=nickname, email=resp.email)
    db.session.add(user)
    db.session.commit()

  remember_me = False
  if 'remember_me' in session:
    remember_me = session['remember_me']
    session.pop('remember_me', None)

  login_user(user, remember = remember_me)
  return redirect(request.args.get('next') or url_for('index'))

# Pages
@app.route('/<slug>')
def view_page(slug):
  page = Page.query.filter_by(slug=slug).first()
  if page is None:
    flash('The URL "%s" was not found' % slug)
    return redirect(url_for('index'))
  return render_template('page.html', page=page)

@app.route('/page/new', methods=['GET', 'POST'])
#@login_required
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
# @login_required
def add_post():
  form = PostForm()

  if form.validate_on_submit():
    flash('Post created: %s' % form.title.data)
    post = Post(title=form.title.data, slug=form.slug.data, body=form.body.data, image=form.image.data)
    db.session.add(post)
    db.session.commit()
    return render_template('post.html', post=post) # TODO: make this a redirect()

  return render_template('new_post.html', form=form)


