# Copyright 2018 Google LLC
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

# [START gae_python37_app]

# open libraries
import cgi
from flask import Flask, request, Response, jsonify, g, redirect
import html

# internal libraries
from helper import *

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

home_html = """
<div class="Udacity_cs253">
    <h1>
        UDACITY course CS253 Problem Sets
    </h1>
    <p class="udacity_cs253_description">
        These are webpages leading to different problem sets for Udacity's course: CS253
    </p>
    <table style="width:100%">
        <tr>
            <td><a href="/cs253/birthday" aria-label="Jump to">CS253 Problem - Birthday</a></td>
            <td><a href="/cs253/unit2/rot13" aria-label="Jump to">CS253 Unit 2 - ROT13</a></td>
            <td><a href="/cs253/unit2/signup" aria-label="Jump to">CS253 Unit 2 - Signup Page</a></td>
        </tr>
    </table>
</div>
"""
birthday_form = """
<form method='post'>
What is your birthday?
<br>
    <label>Month
        <input type='text' name='month' value="%(month)s">
    </label>
    <label>Day
        <input type='text' name='day' value='%(day)s'>
    </label>
    <label>Year
        <input type='text' name='year' value='%(year)s'>
    </label>
    <div style='color: red'>%(error)s</div>
<br>
<input type='submit'>
</form>
"""

rot13_form = """
<form method='post'>
Enter some text to ROT13:
<br>
<textarea name='input'>%(textinput)s</textarea>
<br>
<input type='submit'>
</form>
"""
def write_form(error="", month="", day="", year=""):
    return birthday_form % {"error": cgi.escape(error, quote=True),
                   "month":  cgi.escape(month, quote=True),
                   "day":  cgi.escape(day, quote=True),
                   "year":  cgi.escape(year, quote=True)}

signup_form = """
<h2>Signup</h2>
<br>
<form method = 'POST'>
<label>
    Username
    <input type='text' name='username' value='%(username)s'>
</label>
%(wrong_username_message)s
<br>
<label>
    Password
    <input type='password' name='password' value=''>
</label>
%(wrong_password_message)s
<br>
<label>
    Verify Password
    <input type='password' name='verify_password' value=''>
</label>
%(password_mismatch_message)s
<br>
<label>
    Email (optional)
    <input type='text' name='email' value='%(email)s'>
</label>
%(wrong_email_message)s
<br>
<input type='submit' value='Submit'>
</form>
"""
def write_form_signup(params):
    return signup_form % {**params}

@app.route('/', methods=['GET'])
def home():
    """Return a friendly HTTP greeting."""
    return home_html
    return redirect('/cs253/unit2/signup')

@app.route('/cs253/birthday', methods=['POST','GET'])
def cs253_birthday():
    if request.method == 'POST':
        month = valid_month(request.form['month'])
        day = valid_day(request.form['day'])
        year = valid_year(request.form['year'])
        error = ""
        if not (month and day and year):
            return write_form("That does not valid to me", request.form['month'], request.form['day'], request.form['year'])
        else:
            return redirect('/thanks')
    else:
        """Return a friendly HTTP greeting."""
        return write_form()


@app.route('/testform', methods=['POST', 'GET'])
def test_form():
    if request.method == 'GET':
        user = request.args.get('user')
        return user
        # Response = request
        # return Response #request.data.decode('UTF-8')
    else:
        """Return a friendly HTTP greeting."""
        user = request.form['user']
        return user
        # return 'Got the post request instead of get request'

@app.route('/thanks', methods=['GET'])
def thanks_handler():
    return "Thanks! That's a totally valid day"

@app.route('/cs253/unit2/rot13', methods=['POST','GET'])
def cs_unit2_rot13():
    if request.method == 'GET':
        return rot13_form % {'textinput': ''}
    if request.method == 'POST':
        input = request.form['input']
        return rot13_form % {'textinput': html.escape(rot13_conversion(input), quote=True)}
    else:
        return 'something wrong in post'

@app.route('/cs253/unit2/signup', methods=['POST','GET'])
def user_signup():
    if request.method == 'GET':
        return write_form_signup(params = {
                                'username': '',
                                'email': '',
                                'wrong_username_message':"",
                                'wrong_password_message':"",
                                'password_mismatch_message':"",
                                'wrong_email_message':""})
    elif request.method == 'POST':
        params = {}
        params['username'] = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        params['email'] = request.form['email']
        error = False
        if not IsValidPassword(password):
            params['wrong_password_message'] = "That wasn't a valid password"
            params['password_mismatch_message'] = ""
            error = True
        elif not IsMatchingPassword(password, verify_password):
            params['wrong_password_message'] = ""
            params['password_mismatch_message'] = "Your passwords didn't match"
            error = True
        else:
            params['wrong_password_message'] = ""
            params['password_mismatch_message'] = ""
        if not IsValidUsername(params['username']):
            params['wrong_username_message'] = "That's not a valid username"
            error = True
        else:
            params['wrong_username_message'] = ""
        if not IsValidEmail(params['email']):
            params['wrong_email_message'] = "That's not a valid email"
            error = True
        else:
            params['wrong_email_message'] = ""
        if (error):
            return write_form_signup(params)
        else:
            return redirect('/cs253/unit2/signup/welcome?username=' + params['username'])
    else:
        return 'something wrong in post'

@app.route('/cs253/unit2/signup/welcome', methods=['GET'])
def user_welcome():
    username = request.args.get('username')
    if not IsValidUsername(username) :
        return redirect('/cs253/unit2/signup')
    else:
        return "Welcome, " + username + "!"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=4000, debug=True)
# [END gae_python37_app]
