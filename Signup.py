import re

from BaseHandler import *
from User import *

# Handler for the signup page
class Signup(Handler):
    def get(self):
        self.render("signup-form.html")
    
    def post(self):
        have_error = False
        
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')
        
        params = dict(username = self.username, email = self.email)
        
        if not self.valid_username(self.username):
            params['error_username'] = "Invalid username"
            have_error = True
        
        if not self.valid_password(self.password):
            params['error_password'] = "Invalid password"
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "The passwords do not match."
            have_error = True
        
        if not self.valid_email(self.email):
            params['error_email'] = "Invalid email address"
            have_error = True
        
        if have_error:
            self.render("signup-form.html", **params)
        else:
            self.done()

    def done(self):
        u = User._by_name(self.username)
        if u:
            msg = "The user already exists."
            self.render("signup-form.html", error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login(u)
            self.redirect('/')

    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return username and USER_RE.match(username)

    def valid_password(self, password):
        PASS_RE = re.compile(r"^.{3,20}$")
        return password and PASS_RE.match(password)

    def valid_email(self, email):
        EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        return not email or EMAIL_RE.match(email)

