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
import html


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

form="""
<form method='post'>
Enter some text to ROT13:
<br>
<textarea name='input'>%(textinput)s</textarea>
<br>
<input type='submit'>
</form>
"""

def rot13(input):
    out = ""
    for char in html.unescape(input):
        if (char.isalpha() and char.islower()):
            index = ord(char) - ord('a')
            index = index + 13
            if index > 25:
                index = index - 26
            out = out + chr(index + ord('a'))
        elif char.isalpha():
            index = ord(char) - ord('A')
            index = index + 13
            if index > 25:
                index = index - 26
            out = out + chr(index + ord('A'))
        else:
            out = out + char
    return out

@app.route('/', methods=['POST','GET'])
def home():
    print(request.method)
    if request.method == 'GET':
        return form % {'textinput': ''}
    if request.method == 'POST':
        input = request.form['input']
        return form % {'textinput': html.escape(rot13(input), quote=True)}
    else:
        return 'something wrong in post'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=4000, debug=True)
# [END gae_python37_app]
