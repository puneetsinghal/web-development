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
from flask import Flask, request, Response, jsonify, g, redirect

from helper import *
import cgi


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

form="""
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
def write_form(error="", month="", day="", year=""):
    return form % {"error": cgi.escape(error, quote=True),
                   "month":  cgi.escape(month, quote=True),
                   "day":  cgi.escape(day, quote=True),
                   "year":  cgi.escape(year, quote=True)}

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        month = valid_month(request.form['month'])
        day = valid_day(request.form['day'])
        year = valid_year(request.form['year'])
        error = ""
        # if not month:
        #     error
        if not (month and day and year):
            return write_form("That does not valid to me", request.form['month'], request.form['day'], request.form['year'])
        else:
            return redirect('/thanks')
    else:
        """Return a friendly HTTP greeting."""
        return write_form()

@app.route('/testform', methods=['POST', 'GET'])
def testform():
    print (request)
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
def ThanksHandler():
    return "Thanks! That's a totally valid day"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=4000, debug=True)
# [END gae_python37_app]
