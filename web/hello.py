from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from markupsafe import escape
from flask import abort, redirect, url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World 123!</p>"

@app.route("/<name>", methods=['GET', 'POST'])
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.get('/login')
def login_get():
    return show_the_login_form()

@app.post('/login')
def login_post():
    return do_the_login()

def show_the_login_form():
 return "login form"   

def do_the_login():
    return 'hello, i'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404