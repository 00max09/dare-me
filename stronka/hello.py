from flask import Flask, render_template, redirect, url_for, session
from flask import request, send_from_directory
from models import retrieveUsers, insertUser, insertMovie
from functools import wraps
import sys
import sqlite3
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploaded'
ALLOWED_EXTENSIONS = {'jpg', 'mp4'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "szubert_to_dobra_morda"
DATABASE = "database.db"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return decorator


@app.route('/', methods=['GET'])
@login_required
def home():
    return redirect('/dashboard')

@app.route('/watch')
@login_required
def show_watch():
    return render_template('index.html', data={'filenames': ["koktajl.mp4", "no_spojler.mp4", "first_try.mp4"]})

@app.route('/dashboard')
@login_required
def show_dashboard():
    return render_template('dashboard.html', data={'username': session['username'], 'categories': ['cooking', 'tricks', 'sport', 'education']})

@app.route('/login', methods=['POST', 'GET'])
def login():
    print("login", file=sys.stderr)
    if request.method=='POST':
        print("cewlo", file=sys.stderr)
        username = request.form['username']
        password = request.form['password']
        all_usrs = retrieveUsers()
        if (username, password) in all_usrs:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template("login.html")
    else:
        return render_template('login.html')
# sqlite3 database.db < schema.sql

@app.route('/register',methods=["POST", "GET"])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        insertUser(username, password)
        return redirect("/login")
        
    else:
        return render_template('register.html')

@app.route('/upload',methods=["GET"])
@login_required
def upload():
    # TODO: jak nie ma kategorii to problem to piszemy że jest hakerem i niech przekieruje do haker simularoe
    category = request.args.get('cat')
    return render_template('upload.html', data = {'category':category})

@app.route('/files/<path:name>',methods=["GET"])
def get_video(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@app.route('/upload_file',methods=["POST"])
@login_required
def upload_file():
    file = request.files['file']
    category = request.args.post('cat')

    if file.filename == '':
        return redirect('/upload')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        insertMovie(filename, session['username'], category)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/upload')

if __name__ == '__main__':
    print("all usrs", file=sys.stderr)
    init_db()
    app.run(debug=False, host='0.0.0.0')