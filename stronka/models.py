import sqlite3 as sql

def insertUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users

def insertMovie(filename, username, category):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO movies (moviename,uploader, category, likes) VALUES (?, ?, ?, 0)", (filename, username, category))
    con.commit()
    con.close()