import os
import re
import random
import hashlib
import hmac
import logging
import json
import urllib2

import webapp2
import jinja2

from BaseHandler import *
from User import *
from Post import *
from NewsArticle import *

# Handler for a new post
def getarticles():
    key = '779097b9e35e46b0ac3db6fc358afced'
    sources = ['the-new-york-times', 'the-huffington-post', 'cnn']
    nyt = {}
    huffington = {}
    cnn = {}
    
    for source in sources:
        url = "https://newsapi.org/v1/articles?source=%s&apiKey=%s" % (source, key)
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        first = data['articles'][0]

        if source == 'the-new-york-times':
            nyt = first
        elif source == 'the-huffington-post':
            huffington = first
        elif source == 'cnn':
            cnn = first

    return (nyt, huffington, cnn)
            
        
class NewPost(Handler):
    def render_post(self, title="",
                    title_NYT = "", link_NYT = "", image_NYT = "", description_NYT = "",
                    title_Huffington = "", link_Huffington = "", image_Huffington = "", description_Huffington = "",
                    title_CNN = "", link_CNN = "", image_CNN = "", description_CNN = "",
                    title_Fox = "", link_Fox = "", image_Fox = "", description_Fox = "",
                    title_Breitbart = "", link_Breitbart = "" , image_Breitbart = "", description_Breitbart = "", error=""):
        self.render("newpost.html", title = title,
                    title_NYT = title_NYT, link_NYT = link_NYT, image_NYT = image_NYT, description_NYT = description_NYT,
                    title_Huffington = title_Huffington, link_Huffington = link_Huffington, image_Huffington = image_Huffington, description_Huffington = description_Huffington,
                    title_CNN = title_CNN, link_CNN = link_CNN, image_CNN = image_CNN, description_CNN = description_CNN,
                    title_Fox = title_Fox, link_Fox = link_Fox, image_Fox = image_Fox, description_Fox = description_Fox,
                    title_Breitbart = title_Breitbart, link_Breitbart = link_Breitbart, image_Breitbart = image_Breitbart, description_Breitbart = description_Breitbart, error=error)

    def get(self):
        nyt, huffington, cnn = getarticles()
        self.render_post(title_NYT = nyt['title'], link_NYT = nyt['url'], image_NYT = nyt['urlToImage'], description_NYT = nyt['description'],
                         title_Huffington = huffington['title'], link_Huffington = huffington['url'], image_Huffington = huffington['urlToImage'], description_Huffington = huffington['description'],
                         title_CNN = cnn['title'], link_CNN = cnn['url'], image_CNN = cnn['urlToImage'], description_CNN = cnn['description'])

    def post(self):
        title = self.request.get("title")

        title_NewYorker = self.request.get("title_NewYorker")
        link_NewYorker = self.request.get("link_NewYorker")
        image_NewYorker = self.request.get("image_NewYorker")

        title_NYT = self.request.get("title_NYT")
        link_NYT = self.request.get("link_NYT")
        image_NYT = self.request.get("image_NYT")

        title_Huffington = self.request.get("title_Huffington")
        link_Huffington = self.request.get("link_Huffington")
        image_Huffington = self.request.get("image_Huffington")

        title_CNN = self.request.get("title_CNN")
        link_CNN = self.request.get("link_CNN")
        image_CNN = self.request.get("image_CNN")

        title_Fox = self.request.get("title_Fox")
        link_Fox = self.request.get("link_Fox")
        image_Fox = self.request.get("image_Fox")

        title_Breitbart = self.request.get("title_Breitbart")
        link_Breitbart = self.request.get("link_Breitbart")
        image_Breitbart = self.request.get("image_Breitbart")

        error = ""

        if title and link_NYT and image_NYT and link_Huffington and image_Huffington and link_CNN and image_CNN and link_Fox and image_Fox and link_Breitbart and image_Breitbart:
            post = Post(parent = post_key(), title = title,
                        title_NYT = title_NYT, link_NYT = link_NYT, image_NYT = image_NYT, description_NYT = description_NYT,
                        title_Huffington = title_Huffington, link_Huffington = link_Huffington, image_Huffington = image_Huffington, description_Huffington = description_Huffington,
                        title_CNN = title_CNN, link_CNN = link_CNN, image_CNN = image_CNN, description_CNN = description_CNN,
                        title_Fox = title_Fox, link_Fox = link_Fox, image_Fox = image_Fox, description_Fox = description_Fox,
                        title_Breitbart = title_Breitbart, link_Breitbart = link_Breitbart, image_Breitbart = image_Breitbart, description_Breitbart = description_Breitbart)
            post_id = add_post(post)
            self.redirect('post/%s' % post_id)
        else:
            error = "Invalid input!!!"
            self.render_post(title = title,
                             title_NYT = title_NYT, link_NYT = link_NYT, image_NYT = image_NYT, description_NYT = description_NYT,
                             title_Huffington = title_Huffington, link_Huffington = link_Huffington, image_Huffington = image_Huffington, description_Huffington = description_Huffington,
                             title_CNN = title_CNN, link_CNN = link_CNN, image_CNN = image_CNN, description_CNN = description_CNN,
                             title_Fox = title_Fox, link_Fox = link_Fox, image_Fox = image_Fox, description_Fox = description_Fox,
                             title_Breitbart = title_Breitbart, link_Breitbart = link_Breitbart, image_Breitbart = image_Breitbart, description_Breitbart = description_Breitbart,
                             error=error)

