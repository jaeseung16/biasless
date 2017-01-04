import logging
import json
import urllib2

from google.appengine.ext import ndb

# Class for Post
class Post(ndb.Model):
    # Title & Date and Time for a post
    title = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

    # Links to articles and images
    title_NYT = ndb.StringProperty(required = True)
    link_NYT = ndb.StringProperty(required = True)
    image_NYT = ndb.StringProperty(required = True)

    title_Huffington = ndb.StringProperty(required = True)
    link_Huffington = ndb.StringProperty(required = True)
    image_Huffington = ndb.StringProperty(required = True)

    title_CNN = ndb.StringProperty(required = True)
    link_CNN = ndb.StringProperty(required = True)
    image_CNN = ndb.StringProperty(required = True)

    title_Fox = ndb.StringProperty(required = True)
    link_Fox = ndb.StringProperty(required = True)
    image_Fox = ndb.StringProperty(required = True)

    title_Breitbart = ndb.StringProperty(required = True)
    link_Breitbart = ndb.StringProperty(required = True)
    image_Breitbart = ndb.StringProperty(required = True)

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
