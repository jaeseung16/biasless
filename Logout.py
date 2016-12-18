from BaseHandler import *
            
# Handler for Logout
class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')
