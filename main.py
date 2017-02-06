#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#import webapp2
import re
import cgi

'<!DOCTYPE html>'
'<html lang="en">'
'<head>'
'<meta charset="UTF-8">'
'<title>Signup</title>'
'<link rel="stylesheet" type="text/css" href="Stylez.css"/>'
'<h2>Signup</h2>'

'</head>'
'<body>'
'<form method="post">'
'<table>'
'<tr>'
'<td class="label">'
'Username'
'</td>'
'<td>'
'<input type="text" name="username" value="">'
'</td>'
'<td class="error">'

'</td>'
'</tr>'
'<tr>'
'<td class="label">'
'Password'
'</td>'
'<td>'
'<input type="password" name="password" value="">'
'</td>'
'<td class="error">'
'</td>'
'</tr>'
'<tr>'
'<td class="label">'
'Verify_Password'
'</td>'
'<td>'
'<input type="password" name="verify" value="">'
'</td>'
'<td class="error">'

'</td>'
'</tr>'
'<tr>'
'<td class="label">'
'Email (Optional)'
'</td>'
'<td>'
'<input type="text" name="email" value="">'
'</td>'
'<td class="error">'

'</td>'
'</tr>'

'</table>'
'<input type="Submit" value="Submit">'
'</form>'

'</body>'
'</html>'


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def val_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def val_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def val_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(Basehandler):

    def get(self):
        self.render(user-signup.html)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

    params = dict(username=username,
                  email=email)

if val_username(username):
    params['error_username'] = "That's not a valid username."

else:
    params['error_username'] = ""

if val_password(password):
    params['error_password'] = "That wasn't a valid password."

else:
    params['error_password'] = ""

if password != verify:
    params['error_verify'] = "Your passwords didn't match."

if val_email(email):
    params['error_email'] = "That isn't a valid email."

else:
    params['error_email'] = ""


if have_error:
    self.render('signup-form.html', **params)
else:
    self.redirect('/unit2/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if val_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/unit2/signup')

app = webapp2.WSGIApplication(
    [('/unit2/signup', Signup)
     ('/unit2/welcome', Welcome)],
    debug=True)
