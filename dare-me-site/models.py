import sqlite3 as sql
import sys

def insertUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUserID(name, password):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute(f"SELECT id FROM users WHERE username= \"{name}\" AND password = \"{password}\"")
	user = cur.fetchone()
	con.close()
	return user


def insertMovie(user_id, challenge_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO movies (uploader, challenge_id, likes) VALUES (?, ?, 0)", (user_id, challenge_id))
    con.commit()
    con.close()

def getMaxMovieId():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(id) FROM movies")
    id = cur.fetchone()
    con.close()
    return id[0]

def retrieveAllMovies():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT id, uploader, challenge_id, likes FROM movies ORDER BY likes DESC")
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def retrieveAllCategories():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT id, category_type FROM category")
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def retrieveMoviesByCategory(category_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"""
    SELECT a.id, a.uploader, a.challenge_id, a.likes 
    FROM movies AS a LEFT JOIN challenge AS b
    ON a.challenge_id = b.id
    WHERE b.category_id = {category_id}
    """)
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def retrieveMoviesByUser(user_name):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"SELECT id, uploader, challenge_id, likes FROM movies WHERE uploader = \"{user_name}\"")
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def retrieveChallengesByCategory(category_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"SELECT id, descript, file_id FROM challenge WHERE category_id = {category_id}")
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def insertInstructionMovie(filename):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO instruction_movies (file_name) VALUES (?)", (filename,))
    cur.execute(f"SELECT id FROM instruction_movies WHERE file_name = \"{filename}\"")
    data = cur.fetchone()
    con.commit()
    con.close()
    return data[0]

def retrieveInstructionMovieName(file_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"SELECT file_name FROM instruction_movies WHERE id = {file_id}")
    data = cur.fetchone()
    con.commit()
    con.close()
    return data[0]


def insertChallenge(category_id, descript, file_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO challenge (category_id, file_id, descript) VALUES (?, ?, ?)", (category_id, file_id, descript))
    con.commit()
    con.close()

def personLikePush(film_id, user):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM likes WHERE file_id = {film_id} AND user_id = {user}")
    res = cur.fetchall()
    if len(res) :
        cur.execute(f"DELETE FROM likes WHERE file_id = {film_id} AND user_id = {user}")
    else:
        cur.execute("INSERT INTO likes(user_id, file_id) VALUES (?,?)", (user, film_id))
    con.commit()
    con.close()
       


def getLikes(movie_id, user_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"SELECT COUNT(*) FROM likes WHERE file_id = {movie_id} AND user_id = {user_id}")
    is_liked = cur.fetchone()[0] == 1
    cur.execute(f"SELECT COUNT(*) FROM likes WHERE file_id = {movie_id}")
    likes = cur.fetchone()[0]
    con.commit()
    con.close()
    return (is_liked, likes)

def retrieveAllUsersWithLikes():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"""
    WITH movies_likes as (
        SELECT a.uploader AS uploader, COUNT(*) as likes
        FROM movies as a INNER JOIN likes as b 
        ON a.id = b.file_id
        GROUP BY a.uploader
    )
    SELECT * FROM movies_likes
    WHERE likes > 0 
    ORDER BY likes DESC
    """)
    data = cur.fetchall()
    con.commit()
    con.close()
    return data


def challangeDescById(challange_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"SELECT descript FROM challenge WHERE id = {challange_id}")
    desc = cur.fetchone()[0]
    con.commit()
    con.close()
    return desc

def retrieveCategoryNameById(category_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"SELECT category_type FROM category WHERE id = {category_id}")
    desc = cur.fetchone()[0]
    con.commit()
    con.close()
    return desc

