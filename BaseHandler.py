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
from Comment2 import *
from NewsArticle import *
from Score import *

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
    return ndb.Key('users', group)

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

# Key stuff
def post_key(name = 'default'):
    return ndb.Key('posts', name)

def comment_key(name = 'default'):
    return ndb.Key('comments', name)

def comment2_key(name = 'default'):
    return ndb.Key('comments2', name)

def article_key(name = 'default'):
    return ndb.Key('articles', name)

def score_key(name = 'default'):
    return ndb.Key('scores', name)


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
    mc_key = 'Posts'
    posts, age = age_get(mc_key)
    
    if update or posts is None:
        query = Post.query().order(-Post.created).fetch(limit=12)
        posts = list(query)
        age_set(mc_key, posts)
    
    return posts, age

def add_post(post):
    post.put()
    get_posts(update = True)
    return str(post.key.integer_id())

def get_comments(post_id, update = False):
    mc_key = 'Comments_' + post_id
    comments, age = age_get(mc_key)
    
    if update or comments is None:
        query = Comment.query().filter(Comment.post_id == post_id).order(-Comment2.created).fetch(limit=10)
                                       
        if query:
            comments = list(query)
            age_set(mc_key, comments)
            logging.warning('There are comments.')
        else:
            comments = None
            logging.warning('There is no comments.')

    return comments, age

def add_comment(comment):
    logging.warning('Comment added')
    comment.put()
    get_comments(post_id = comment.post_id, update = True)
    
    return str(comment.key.integer_id())

def get_comments2(article_id, update = False):
    mc_key = 'Comment2_' + article_id
    comments2, age = age_get(mc_key)
    
    if update or comments2 is None:
        query = Comment2.query().filter(Comment2.article_id == article_id).order(-Comment2.created).fetch(limit=10)
        comments2 = list(query)
        age_set(mc_key, comments2)
    
    return comments2, age

def add_comment2(comment2):
    comment2.put()
    get_comments2(article_id = comment2.article_id, update = True)
    
    return str(comment2.key.integer_id())

def get_articles(update = False):
    mc_key = 'NewsArticles'
    articles, age = age_get(mc_key)
    
    if update or articles is None:
        query = NewsArticle.query().order(-NewsArticle.created).fetch(limit=30)
        articles = list(query)
        
        if len(articles) == 0:
            articles = read_from_example2()
        
        age_set(mc_key, articles)
    
    return articles, age

def add_article(article):
    article.put()
    get_articles(update = True)
    return str(article.key.integer_id())

def read_from_example2():
    key = '779097b9e35e46b0ac3db6fc358afced'
    sources = ['the-new-york-times', 'the-huffington-post', 'cnn']
    newsarticles = []
    
    for source in sources:
        url = "https://newsapi.org/v1/articles?source=%s&apiKey=%s" % (source, key)
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        articles = data['articles']
        
        for article in articles:
            a = NewsArticle(parent = article_key(), title = article['title'],
                            source = source, url = article['url'], image = article['urlToImage'],
                            description = article['description'], score = '0.00', total_score = 0.0, no_scored = 0)
            a.put()
            newsarticles.append(a)
    
    return newsarticles

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
        self.set_secure_cookie('user_id', str(user.key.integer_id()))
    
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
    
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User._by_id(int(uid))
        
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'
