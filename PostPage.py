from BaseHandler import *

from User import *
from Post import *
from Comment import *

# Handler for individual posts
class PostPage(Handler):
    def render_post(self, post_id = None, error = ""):
        postkey = 'POST_' + post_id
        post, age = age_get(postkey)
        
        if not post:
            key = ndb.Key('Post', int(post_id), parent = post_key())
            post = key.get()
            logging.warning('not yet in the memcache')
            age_set(postkey, post)
            age = 0
        
        if not post:
            self.error(404)
            return
        elif self.format == 'html':
            comments, age = get_comments(post_id)
            logging.warning('%s' % age)
            #logging.warning('Postpage %s' % len(comments))
            logging.warning('set %s' % len(list(Comment.query().filter(Comment.post_id == post_id).order(-Comment.created).fetch(limit=10))) )
            
            if comments == None:
                comments = []
            
            if self.user:
                self.render("permalink.html", post = post, username = self.user.name, comments = comments, error = error)
            else:
                #logging.warning("Something wrong")
                self.render("permalink.html", post = post, username = None, comments = comments, error = error)
        else:
            comments, age = get_comments(post_id)
            
            if comments:
                self.render_json([post.as_dict()] + [c.as_dict() for c in comments])
            else:
                self.render_json([post.as_dict()])

    
    def get(self, post_id):
        self.render_post(post_id = post_id)
    
    def post(self, post_id):
        error = ''
        comments = ''
        postkey = 'POST_' + post_id
        post, age = age_get(postkey)
        
        if self.user:
            username = self.request.get("username")
            if self.user.name == username:
                comment = self.request.get("comment")
                
                if comment:
                    c = Comment(parent = comment_key(), user_id = str(self.user.key.integer_id()), username = username, post_id = str(post.key.integer_id()), comment = comment, score = '0.00', total_score = 0.0, no_scored = 0)
                    add_comment(c)
                
                else:
                    error = 'Please write your comment.'
            else:
                error = "The username does not match."
                
        else:
            error = "Please login to submit your comment."
        
        self.render_post(post_id = post_id, error = error)
