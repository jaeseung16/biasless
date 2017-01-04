import hashlib
import random

from string import letters

from google.appengine.ext import ndb

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

# Class for User
class User(ndb.Model):
    name = ndb.StringProperty(required = True)
    pw_hash = ndb.StringProperty(required = True)
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add = True)
    score = ndb.IntegerProperty()
    
    @classmethod
    def _by_id(cls, uid):
    	return User.get_by_id(uid, parent = users_key())
    	
    @classmethod
    def _by_name(cls, name):
        return User.query().filter(cls.name == name).get()
    
    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(), name = name, pw_hash = pw_hash, email = email)
    	
    @classmethod
    def login(cls, name, pw):
        u = cls._by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
