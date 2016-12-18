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
            key = db.Key.from_path('Post', int(post_id), parent = post_key())
            post = db.get(key)
            age_set(postkey, post)
            age = 0
        
        if not post:
            self.error(404)
            return
        elif self.format == 'html':
            comments, age = get_comments(post_id)
            logging.warning('Postpage %s' % len(comments))
            logging.warning('set %s' % len(list(Comment.all().filter('post_id =', post_id).order('-created').fetch(limit=10))) )
            
            if self.user:
                self.render("permalink.html", post = post, username = self.user.name, comments = comments, error = error)
            else:
                self.render("permalink.html", post = post, username = None, comments = comments, error = error)
        else:
            comments, age = get_comments(post_id)
            self.render_json([post.as_dict()] + [c.as_dict() for c in comments])

    
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
                    c = Comment(parent = comment_key(), user_id = str(self.user.key().id()), username = username, post_id = str(post.key().id()), comment = comment)
                    add_comment(c)
                
                else:
                    error = 'Please write your comment.'
            else:
                error = "The username does not match."
                
        else:
            error = "Please login to submit your comment."
        
        self.render_post(post_id = post_id, error = error)
