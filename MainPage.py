from BaseHandler import *

from User import *
from Post import *

# Handler for the main page
class MainPage(Handler):
    def get(self):
        error = ''
        posts, age = get_posts()
        
        if self.format == 'html':
            logging.warning('Mainpage %s' % len(posts))
            logging.warning('Mset %s' % len(list(Post.query()) ))
            if self.user:
                self.render('content.html', posts = posts, username = self.user.name, error = error)
            else:
                self.render('content.html', posts = posts, username = None, error = error)
        else:
            return self.render_json([p.as_dict() for p in posts])
