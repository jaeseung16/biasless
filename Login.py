from BaseHandler import *
from User import *

# Handler for Login
class Login(Handler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)
            
# Handler for Logout
class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')
