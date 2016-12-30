from BaseHandler import *

# Handler for the main page
class MainPage2(Handler):
    def get(self):
        error = ''
        articles, age = get_articles()
        
        if self.format == 'html':
            #logging.warning('Mainpage %s' % len(posts))
            #logging.warning('Mset %s' % len(list(Post.all()) ))
            if self.user:
                self.render('content2.html', articles = articles, username = self.user.name, error = error)
            else:
                self.render('content2.html', articles = articles, username = None, error = error)
        else:
            return self.render_json([p.as_dict() for article in articles])
