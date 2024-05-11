import re

from flask import Flask, session, render_template, redirect, request

from views1.page import page
from views1.user import user

app = Flask(__name__)
app.secret_key = 'This is a app.secret_Key , You Know ?'

app.register_blueprint(page.pb)
app.register_blueprint(user.ub)


@app.route('/')
def index():
    return redirect('/user/login')


@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat, request.path):
        return
    if request.path == '/user/login':
        return
    if request.path == '/user/register':
        return
    uname = session.get('username')
    if uname:
        return None

    return redirect('/user/login')


@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
