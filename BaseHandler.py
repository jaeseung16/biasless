import os
import hmac
import logging

import webapp2
import jinja2

from google.appengine.api import memcache
from datetime import datetime, timedelta

from User import *
from Post import *
from Comment import *

# Set the template folder
template_dir = os.path.join( os.path.dirname(__file__), 'templates')

# For the jinja2 environment
jinja_env = jinja2.Environment( loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

# keys - should be moved to other files
secret = 'cUPU9sx9AM'

# Cookie stuff
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

# User stuff
def users_key(group = 'default'):
    return db.Key.from_path('users', group)

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

# Post stuff
def post_key(name = 'default'):
    return db.Key.from_path('posts', name)

# Comment stuff
def comment_key(name = 'default'):
    return db.Key.from_path('comments', name)

# Memcache stuff
def age_set(key, val):
    save_time = datetime.utcnow()
    memcache.set(key, (val, save_time))

def age_get(key):
    r = memcache.get(key)
    if r:
        val, save_time = r
        age = (datetime.utcnow() - save_time).total_seconds()
    else:
        val, age = None, 0
    
    return val, age

def get_posts(update = False):
    mc_key = 'Post'
    posts, age = age_get(mc_key)
    
    if update or posts is None:
        query = Post.all().order('-created').fetch(limit=5)
        posts = list(query)
        
        if len(posts) == 0:
            posts, age = read_from_example()
        
        age_set(mc_key, posts)
    
    return posts, age

def add_post(post):
    post.put()
    get_posts(update = True)
    return str(post.key().id())

def get_comments(post_id, update = False):
    mc_key = 'Comment_' + post_id
    comments, age = age_get(mc_key)
    
    if update or comments is None:
        query = Comment.all().filter('post_id =', post_id).order('-created').fetch(limit=10)
        comments = list(query)
        age_set(mc_key, comments)
    
    return comments, age

def add_comment(comment):
    comment.put()
    get_comments(post_id = comment.post_id, update = True)
    
    return str(comment.key().id())


# Handler
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)
    
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))
    
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)
    
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
    
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
    
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
        
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'
