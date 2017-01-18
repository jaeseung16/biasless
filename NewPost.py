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
            newsarticles.append(a)

    return newsarticles
            
        
class NewPost(Handler):
    def get(self):
        error = ''
        articles = getarticles()
        age_set('TempArticles', articles)

        if self.user:
            self.render('newpost.html', articles = articles, username = self.user.name, error = error)
        else:
            self.render('newpost.html', articles = articles, username = None, error = error)

    def post(self):
        error = ''
        idx = self.request.get_all("article")
        
        articles, age = age_get('TempArticles')
        logging.warning('%s' % len(articles))

        if idx:
            articles_to_add = []
            articlesID = []
            for i in idx:
                article = articles[int(i)]
                a = NewsArticle(parent = article_key(), title = article.title,
                                source = article.source, url = article.url, image = article.image,
                                description = article.description, score = '0.00', total_score = 0.0, no_scored = 0)
                a.put()
                articlesID.append( str(a.key.integer_id()) )
                articles_to_add.append(a)

            post = Post(parent = post_key(), articles = articles_to_add, articlesID = articlesID)
            post_id = add_post(post)
            
            self.redirect('post/%s' % post_id)
        else:
            error = "Invalid input!!!"
            if self.user:
                self.render('newpost.html', articles = articles, username = self.user.name, error = error)
            else:
                self.render('newpost.html', articles = articles, username = None, error = error)
