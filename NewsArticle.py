import logging
import json
import urllib2

from google.appengine.ext import db

# Class for Comment

class NewsArticle(db.Model):
    created = db.DateTimeProperty(auto_now_add = True)
    title = db.StringProperty(required = True)
    source = db.StringProperty(required = True)
    url = db.LinkProperty(required = True)
    image = db.LinkProperty(required = True)
    description = db.StringProperty()
    score = db.FloatProperty()

    def as_dict(self):
        time_fmt = '%c'
        d = {'created': self.created.strftime(time_fmt), 'title': self.title,
            'url': self.url, 'image': self.image, 'description': self.description, 'score': self.score}
        return d
