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
import datetime
from flask import Flask, request, Response, jsonify, g, redirect, render_template, url_for
import html
from google.cloud import datastore

# internal libraries
from helper import *
from hash import *
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

client = datastore.Client()

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
            <td><a href="/cs253/birthday" aria-label="Jump to">Problem - Birthday</a></td>
            <td><a href="/cs253/unit2/rot13" aria-label="Jump to">Unit 2 - ROT13</a></td>
            <td><a href="/cs253/unit2/signup" aria-label="Jump to">Unit 2 - Signup Page</a></td>
            <td><a href="/cs253/templates/shopping_list_1" aria-label="Jump to">Problem - Shopping List 1</a></td>
            <td><a href="/cs253/templates/shopping_list_2" aria-label="Jump to">Problem - Shopping List 2</a></td>
            <td><a href="/cs253/templates/ascii" aria-label="Jump to">Problem - ASCII Chan</a></td>
            <td><a href="/cs253/blog" aria-label="Jump to">Problem - Blog</a></td>
            <td><a href="/cs253/unit3/signup" aria-label="Jump to">Unit 3 - Signup </a></td>
        </tr>
    </table>
    <br>
    <div class="error">
        {}
    </div>
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

list_input_form = """
<h1>Add a Food</h1>
<form>
<input type="text" name="food">
%s
<input type="submit" value="Add">
</form>
"""
hidden_item = """
<input type="hidden" name="food" value="%s">
"""
item_list = "<li>%s</li>"

shopping_list = """
<br>
<br>
<h1>Shopping List</h1>
<ul>
%s
<ul>
"""
def write_form_signup(params):
    return signup_form % {**params}

@app.route('/', methods=['GET'])
def home():
    """Return a friendly HTTP greeting."""
    response = Response()
    response.headers['Content-Type'] = 'text/html'
    request_visits_cookie = request.cookies.get('visits')
    visits = 0
    if request_visits_cookie:
        val = check_secure_val(request_visits_cookie)
        if val:
            visits = int(val) + 1
    message = 'You have been here %s times' % visits
    response.headers.add_header('Set-Cookie', 'visits=%s' % make_secure_val(visits))
    response.data = home_html.format(message)
    return response

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

@app.route('/cs253/templates/shopping_list_1', methods=['GET'])
def shopping_list_1():
    food = request.args.getlist("food")
    items_output = ""
    hidden_output = ""
    for item in food:
        hidden_output += hidden_item % item
        items_output += item_list % item
    shopping_list_output = shopping_list % items_output
    return list_input_form % hidden_output + shopping_list_output

@app.route('/cs253/templates/shopping_list_2', methods=['GET'])
def shopping_list_2():
    items = request.args.getlist("food")
    return render_template('shopping_list.html', items=items)

@app.route('/cs253/templates/ascii', methods=['GET', 'POST'])
def ascii():
    if request.method == 'GET':
        items = client.query().fetch()
        return render_template("ascii_chan.html", items=items)
    elif request.method == 'POST':
        title = request.form["title"]
        art = request.form["art"]
        if art and title:
            # key = client.key('EntityKind', "ascii-chan")
            entity = datastore.Entity(key=client.key('ascii-chan', title))
            entity.update({'title': title, 'art': art})
            client.put(entity)
            items = client.query().fetch()
            return render_template("ascii_chan.html", items=items)
        else:
            error = "we need title as well some artwork"
            items = client.query().fetch()
            return render_template("ascii_chan.html", title=title, art=art, error=error, items=items)

@app.route('/cs253/blog/newpost', methods=['GET', 'POST'])
def blog_newpost():
    if request.method == 'GET':
        items = client.query().fetch()
        return render_template("blog-newpost.html")
    elif request.method == 'POST':
        subject = request.form["subject"]
        blog = request.form["blog"]
        if subject and blog:
            entity = datastore.Entity(key=client.key('blog'))
            entity.update({'subject': subject, 'blog': blog, "created":datetime.datetime.utcnow()})
            client.put(entity)
            return redirect('/cs253/blog/' + str(entity.id))
        else:
            error = "subject and content should not be empty!"
            return render_template("blog-newpost.html", subject=subject, blog=blog, error=error)

@app.route('/cs253/blog', methods=['GET'])
def blog_front():
    items = client.query(kind='blog', order=["-created"]).fetch()
    return render_template("blog-front.html", items=items)

@app.route('/cs253/blog/<id>', methods=['GET'])
def blog_post(id):
    query = client.query(kind='blog')
    items = [item for item in query.fetch() if item.id == int(id)]
    return render_template("blog-permalink.html", item=items[0])

@app.route('/cs253/unit3/signup', methods=['POST','GET'])
def unit3_signup():
    if request.method == 'GET':
        return render_template("unit3_signup.html")
    elif request.method == 'POST':
        params = {}
        params['username'] = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        params['email'] = request.form['email']
        error = False
        if not IsValidPassword(password):
            params['wrong_password_message'] = "That wasn't a valid password"
            error = True
        elif not IsMatchingPassword(password, verify_password):
            params['password_mismatch_message'] = "Your passwords didn't match"
            error = True
        if not IsValidUsername(params['username']):
            params['wrong_username_message'] = "That's not a valid username"
            error = True
        if not IsValidEmail(params['email']):
            params['wrong_email_message'] = "That's not a valid email"
            error = True
        if (error):
            return render_template("unit3_signup.html", **params)
        else:
            query = client.query(kind='users', filters=[('username', '=', params['username'])])
            if len(list(query.fetch())) != 1:
                return render_template('unit3_signup.html', username=params['username'], wrong_username_message="That user already exists.")
            entity = datastore.Entity(key=client.key('users'))
            entity.update({\
                'username': params['username'],\
                'password': make_password_hash(params['username'], password),\
                'email': params['email']})
            client.put(entity)
            response = redirect('cs253/unit3/welcome')
            cookie = make_secure_val(entity.id)
            response.headers.add_header('Set-Cookie', 'user_id=%s' % cookie)
            return response #redirect(url_for('unit3_welcome', username=params['username']))
    else:
        return 'something wrong in post'

@app.route('/cs253/unit3/welcome', methods=['GET'])
def unit3_welcome():
    cookie = request.cookies.get('user_id')
    username = check_secure_val(cookie)
    if username.isdigit():
        username = int(username)
    if not username:
        return redirect('cs253/unit3/signup')
    query = client.query(kind='users')
    entity = [item for item in query.fetch() if item.id == username]
    if (len(entity) != 1):
        print("ERROR! username is not found in database")
    entity = entity[0]
    response = Response()
    response.headers['Content-Type'] = 'text/html'
    response.headers.add_header('Set-Cookie', 'user_id=%s' %(cookie))
    response.data = render_template('unit3_welcome.html', username=username)
    return response

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=4000, debug=True)
# [END gae_python37_app]
