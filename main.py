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
import webapp2
import re
import cgi


header = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Signup</title>
<link rel="stylesheet" type="text/css" href="Stylez.css"/>'''

title = '''<h2>Signup</h2>'''

main = '''</head>
<body>
<form method="post">
<table>
<tr>
<td class="label">
Username
</td>
<td>
<input type="text" name="username" value="">
</td>
<td class="error">
%(error_username)s
</td>
</tr>
<tr>
<td class="label">
Password
</td>
<td>
<input type="password" name="password" value="">
</td>
<td class="error">
%(error_password)s
</td>
</tr>
<tr>
<td class="label">
Verify Password
</td>
<td>
<input type="password" name="verify" value="">
</td>
<td class="error">
%(error_verify)s
</td>
</tr>
<tr>
<td class="label">
Email (Optional)
</td>
<td>
<input type="text" name="email" value="">
</td>
<td class="error">
%(error_email)s
</td>
</tr>
</table>
<input type="Submit" value="Submit">
</form>'''

footer = '''</body>
</html>'''

welcome = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Unit 2 Signup</title>
</head>
<body>
    <h2>Welcome, %(username)s!</h2>
</body>
</html>'''


def escape_main(s):
    return cgi.escape(s, quote=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def val_username(username):

    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")


def val_password(password):
    return password and PASS_RE.match(password)


EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def val_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(webapp2.RequestHandler):
    def write_form(self, error_username="", error_password="", error_verify="", error_email="", username="",
                   email=""):
        self.response.out.write(main % {'error_username': error_username,
                                        'error_password': error_password,
                                        'error_verify': error_verify,
                                        'error_email': error_email,
                                        'username': escape_main(username),
                                        'email': escape_main(email)
                                        })

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')


        if not val_username(username):
            error_username = "That's not a valid username."
            have_error = True
        else:
            error_username = ""

        if not val_password(password):
            error_password = "That wasn't a valid password."
            have_error = True
        else:
            error_password = ""

        if password != verify:
            error_verify = "Your passwords didn't match."
            have_error = True
        else:
            error_verify = ""

        if not val_email(email):
            error_email = "That isn't a valid email."
            have_error = True
        else:
            error_email = ""

        if have_error:
            self.write_form(error_username, error_password, error_verify, error_email, username, email)

        else:
            self.redirect('/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = escape_main(self.request.get('username'))
        self.response.write('<h1>Welcome, ' + username + '!</h1>')

app = webapp2.WSGIApplication(
    [('/signup', Signup),
     ('/welcome', Welcome)],
    debug=True)
