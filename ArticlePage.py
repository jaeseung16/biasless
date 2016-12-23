from BaseHandler import *

from User import *
from NewsArticle import *
from Comment2 import *

# Handler for individual posts
class ArticlePage(Handler):
    def render_post(self, article_id = None, error = ""):
        articlekey = 'ARTICLE_' + article_id
        article, age = age_get(articlekey)
        
        if not article:
            key = db.Key.from_path('NewsArticle', int(article_id), parent = article_key())
            article = db.get(key)
            age_set(articlekey, article)
            age = 0
        
        if not article:
            self.error(404)
            return
        elif self.format == 'html':
            comments2, age = get_comments2(article_id)
            logging.warning('Articlepage %s' % len(comments2))
            logging.warning('set %s' % len(list(Comment2.all().filter('article_id =', article_id).order('-created').fetch(limit=10))) )
            
            if self.user:
                self.render("permalink2.html", article = article, username = self.user.name, comments2 = comments2, error = error)
            else:
                self.render("permalink2.html", article = article, username = None, comments2 = comments2, error = error)
        else:
            comments2, age = get_comments2(article_id)
            self.render_json([article.as_dict()] + [c.as_dict() for c in comments2])

    
    def get(self, article_id):
        self.render_post(article_id = article_id)
    
    def post(self, article_id):
        error = ''
        comments2 = ''
        articlekey = 'ARTICLE_' + article_id
        article, age = age_get(articlekey)
        
        if self.user:
            username = self.request.get("username")
            if self.user.name == username:
                comment2 = self.request.get("comment")
                
                if comment2:
                    c = Comment2(parent = comment2_key(), user_id = str(self.user.key().id()), username = username, article_id = str(article.key().id()), comment = comment2)
                    add_comment2(c)
                
                else:
                    error = 'Please write your comment.'
            else:
                error = "The username does not match."
                
        else:
            error = "Please login to submit your comment."
        
        self.render_post(article_id = article_id, error = error)
