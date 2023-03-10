from flask import Flask, render_template, redirect, url_for, session, jsonify
from flask import request, send_from_directory
from models import retrieveCategoryNameById, challangeDescById, personLikePush, getLikes, insertChallenge, insertInstructionMovie, insertUser, insertMovie, getMaxMovieId, retrieveAllMovies, retrieveMoviesByCategory, retrieveAllCategories, retrieveChallengesByCategory, retrieveInstructionMovieName, retrieveUserID, retrieveMoviesByUser, retrieveAllUsersWithLikes
from functools import wraps
import sqlite3
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploaded'
ALLOWED_EXTENSIONS = {'mp4'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "very secret key"
DATABASE = "database.db"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'username' in session and session['username'] == 'a':
            return f(*args, **kwargs)
        elif 'username' in session:
            return redirect('/dashboard')
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
    movies = retrieveAllMovies()
    return render_template('watch.html', data={'movies': addChallDesc(movies)})

@app.route('/watch/<category_id>')
@login_required
def show_watch_category(category_id):
    movies = retrieveMoviesByCategory(category_id)
    return render_template('watch.html', data={'movies': addChallDesc(movies)})

@app.route('/watch_user/<username>')
@login_required
def show_watch_user(username):
    movies = retrieveMoviesByUser(username)
    return render_template('watch.html', data={'movies': addChallDesc(movies)})

@app.route('/like/<film_id>', methods=['POST'])
@login_required 
def like(film_id):
    personLikePush(int(film_id), session['user_id'])
    return ""

@app.route("/get_likes/<movie_id>")
@login_required
def get_like(movie_id):
    is_liked, likes = getLikes(movie_id, session['user_id'])
    return jsonify({"is_liked": is_liked, "likes": likes})


@app.route('/dashboard')
@login_required
def show_dashboard():
    categories = retrieveAllCategories()
    return render_template('dashboard.html', data={'username': session['username'], 'categories': categories})

@app.route('/hall_of_fame')
@login_required
def show_hall_of_fame():
    users_with_likes = retrieveAllUsersWithLikes()
    return render_template('hall_of_fame.html', data={'users_with_likes': users_with_likes})


@app.route('/category/<category_id>')
@login_required
def show_category(category_id):
    challenges_list = retrieveChallengesByCategory(category_id)
    category_name = retrieveCategoryNameById(category_id)
    return render_template('category.html', data={'username': session['username'], 'challenges': challenges_list, 'category_name': category_name})

@app.route('/challengedesc/<file_id>')
@login_required
def show_desc(file_id):
    filename = retrieveInstructionMovieName(file_id)
    return render_template('watch_singular.html', data={"filename": filename})

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user_id = retrieveUserID(username, password)
        if user_id is not None:
            session['username'] = username
            session['user_id'] = user_id[0]
            return redirect('/dashboard')
        else:
            return render_template("login.html")
    else:
        return render_template('login.html')

@app.route('/register',methods=["POST", "GET"])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        insertUser(username, password)
        return redirect("/login")
        
    else:
        return render_template('register.html')

@app.route('/upload/<challenge_id>',methods=["GET"])
@login_required
def upload(challenge_id):
    return render_template(f'upload.html', data = {'id':challenge_id})

@app.route('/files/<path:name>',methods=["GET"])
def get_video(name):
    if name[-4:] != '.mp4':
        name += '.mp4'
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@app.route('/upload_file',methods=["POST"])
@login_required
def upload_file():
    file = request.files['file']
    challenge_id = request.form['cat']
    if file.filename == '':
        return redirect(f'/upload/{challenge_id}')

    if file and allowed_file(file.filename):
        insertMovie(session['username'], challenge_id)
        file.filename = str(getMaxMovieId()) + ".mp4"
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/dashboard')
    else:
        return redirect(f'/upload/{challenge_id}')

@app.route('/upload_challenge',methods=["GET", "POST"])
@admin_required
def upload_challenge():
    if request.method=='GET':
        categories = retrieveAllCategories()
        return render_template('upload_challenge.html', data = {"categories": categories})
    else:
        file = request.files['file']
        if file and allowed_file(file.filename):
            category_id = request.form['category']
            descript = request.form['desc']
            filename = secure_filename(file.filename)
            file_id = insertInstructionMovie(filename)
            insertChallenge(category_id, descript, file_id)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/dashboard')


@app.route('/logout',methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect('/login')



def addChallDesc(movies):
    return [(id, uploader, challangeDescById(challenge_id), likes) for (id, uploader, challenge_id, likes) in movies]


if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0')


