import logging
import json
import urllib2

from google.appengine.ext import db

# Class for Comment

class Comment(db.Model):
    created = db.DateTimeProperty(auto_now_add = True)
    user_id = db.StringProperty(required = True)
    username = db.StringProperty(required = True)
    post_id = db.StringProperty(required = True)
    comment = db.StringProperty(required = True) # Maximum length of a comment = 1500 bytes

    def as_dict(self):
        time_fmt = '%c'
        d = {'user_id': self.user_id, 'username': self.username, 'post_id': self.post_id, 'created': self.created.strftime(time_fmt), 'comment': self.comment}
        return d
