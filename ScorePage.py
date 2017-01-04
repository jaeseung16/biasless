from BaseHandler import *

from User import *
from NewsArticle import *
from Score import *

# Handler for individual posts
class ScorePage(Handler):
    def render_post(self, article = "", score="", error = ""):
        self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('%0.2f' % float(score) )
        self.render("score.html", article = article, score = score)
    
    def get(self, article_id):
        logging.warning("Hello %s" % article_id)

    
    def post(self, article_id):
        if self.user:
            username = self.request.get("username")
            score = self.request.get("score")
            user_id = str(self.user.key().id())

            article = NewsArticle.get_by_id(id = long(article_id), parent = article_key())
            article.total_score += float(score)
            article.no_scored += 1
            temp = article.total_score / float( article.no_scored )
            article.score = '%.2f' % temp
            logging.warning("Hello %s / %s = %s" % (article.total_score, article.no_scored, article.score) )
            add_article(article)
            articlekey = 'ARTICLE_' + article_id
            age_set(articlekey, article)

            s = Score(parent = score_key(), user_id = user_id, article_id = article_id, score = float(score) )
            s.put()
            scorekey = 'SCORE_' + article_id + '_' + user_id
            age_set(scorekey, s)
            logging.warning('scorekey = %s' % scorekey)

            self.render_post(article = article, score = s)


