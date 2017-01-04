from BaseHandler import *

from User import *
from NewsArticle import *
from Comment2 import *

# Handler for individual posts
class ArticlePage(Handler):
    def render_post(self, article_id = None, score="", error = ""):
        articlekey = 'ARTICLE_' + article_id
        article, age = age_get(articlekey)

        if self.user:
            user_id = str(self.user.key().id())
            scorekey = 'SCORE_' + article_id + '_' + user_id
            score, age_score = age_get(scorekey)
            # Add here to deal with the case when score is None.
            logging.warning('scorekey = %s' % score)
        
        if not article:
            key = ndb.Key('NewsArticle', int(article_id), parent = article_key())
            article = key.get()
            age_set(articlekey, article)
            age = 0
            logging.warning('Score %s' % article.score)
        
        if not article:
            self.error(404)
            return
        elif self.format == 'html':
            comments2, age = get_comments2(article_id)
            logging.warning('Articlepage %s' % len(comments2))
            logging.warning('set %s' % len(list(Comment2.query().filter(Comment2.article_id == article_id).order(-Comment2.created).fetch(limit=10))) )
            logging.warning('Score %s' % article.score)
            
            if self.user:
                self.render("permalink2.html", article = article, username = self.user.name, comments2 = comments2, no_comments = len(comments2), score = score, error = error)
            else:
                self.render("permalink2.html", article = article, username = None, comments2 = comments2, no_comments = len(comments2), score = score, error = error)
        else:
            comments2, age = get_comments2(article_id)
            self.render_json([article.as_dict()] + [c.as_dict() for c in comments2])

    
    def get(self, article_id):
        self.render_post(article_id = article_id)
    
    def post(self, article_id):
        error = ''
        comments2 = ''
        score = ''
        #articlekey = 'ARTICLE_' + article_id
        #article, age = age_get(articlekey)
        
        if self.user:
            username = self.request.get("username")
            if self.user.name == username:
                comment2 = self.request.get("comment")
                logging.warning('Score %s' % score)
                
                if comment2:
                    c = Comment2(parent = comment2_key(), user_id = str(self.user.key().id()), username = username, article_id = article_id, comment = comment2)
                    add_comment2(c)
                
                else:
                    error = 'Please write your comment.'
        
                if score:
                    error = score
            else:
                error = "The username does not match."
                
        else:
            error = "Please login to submit your comment."
        
        self.render_post(article_id = article_id, score = score, error = error)


