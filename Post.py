import logging
import json
import urllib2

from google.appengine.ext import db

# Class for Post
class Post(db.Model):
    # Title & Date and Time for a post
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    # Links to articles and images
    title_NYT = db.StringProperty(required = True)
    link_NYT = db.LinkProperty(required = True)
    image_NYT = db.LinkProperty(required = True)

    title_Huffington = db.StringProperty(required = True)
    link_Huffington = db.LinkProperty(required = True)
    image_Huffington = db.LinkProperty(required = True)

    title_CNN = db.StringProperty(required = True)
    link_CNN = db.LinkProperty(required = True)
    image_CNN = db.LinkProperty(required = True)

    title_Fox = db.StringProperty(required = True)
    link_Fox = db.LinkProperty(required = True)
    image_Fox = db.LinkProperty(required = True)

    title_Breitbart = db.StringProperty(required = True)
    link_Breitbart = db.LinkProperty(required = True)
    image_Breitbart = db.LinkProperty(required = True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'title': self.title,
             'NewYorkTimes': {'title': self.title_NYT, 'link': self.link_NYT, 'image': self.image_NYT},
             'HuffingtonPost': {'title': self.title_Huffington, 'link': self.link_Huffington, 'image': self.image_Huffington},
             'CNN': {'title': self.title_CNN, 'link': self.link_CNN, 'image': self.image_CNN},
             'FoxNews': {'title': self.title_Fox, 'link': self.link_Fox, 'image': self.image_Fox},
             'Breitbart': {'title': self.title_Breitbart, 'link': self.link_Breitbart, 'image': self.image_Breitbart},
             'created': self.created.strftime(time_fmt)}
        return d
