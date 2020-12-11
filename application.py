from flask import Flask, render_template, request, redirect, url_for, session
import time
import os
from cs50 import SQL
import dataset
import pandas as pd
import psycopg2

app = Flask(__name__)
# TODO: connect your database here
db = dataset.connect("postgres://ddwbsshctrcopd:5873de1bae81aa8dd1c1680475d0f7a1674dd3ceb057f0c285c81179783333e7@ec2-174-129-224-33.compute-1.amazonaws.com:5432/d32641cd2da4vv")
app.secret_key = 'iq873g'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def home():
	return render_template ("home.html")
	
@app.route('/home')
def homepage():
	return render_template('home.html')

@app.route('/about')
def aboutt():
	return render_template('about.html')

@app.route('/contact')
def con():
	return render_template ("contact.html")

# TODO: route to /list
@app.route('/list')
def listt():
	if "username" in session:
		usersTable = db["users"]
		allusers = list (usersTable.all())[::-1]
		return render_template ("list.html" , allusers=allusers )
	else:
		viewlist= True
		return render_template("login.html", viewlist= viewlist)

# TODO: route to /feed
@app.route('/feed', methods= ["GET","POST"])
def newsFeed():
	posts=db["posts"]
	allposts = list(posts.all())[::-1]
	
	if "username" in session:
		if request.method == "GET":
			return render_template("feed.html", allposts=allposts)
		else:
			form=request.form
			username = session['username']
			post=form["post"]
			time_string = time.strftime('%l:%M on %b %d, %Y')
			entry = {"username":username, "post": post, "time_string" : time_string}
			posts.insert(entry)
			allposts = list(posts.all())[::-1]
			return render_template("feed.html", allposts=allposts)
	else:
		viewnewsfeed= True
		return render_template("login.html", viewnewsfeed= viewnewsfeed)

# TODO: route to /register
@app.route('/register', methods=["GET", "POST"])
def regist():
	if request.method == "GET":
		return render_template ("register.html")
	else:
		form = request.form
		usersTable = db["users"]
		firstname = form["firstname"]
		lastname = form["lastname"]
		username= form["username"]
		email = form["email"]
		hometown = form["hometown"]
		personalwebsite = form["personalwebsite"]
		password = form["password"]
		entry = {"firstname":firstname , "lastname":lastname, "username":username , "email":email , "hometown":hometown , "personalwebsite":personalwebsite, "password":password}
		nameToCheck = username
		results = list(usersTable.find(username = nameToCheck))
		print (len(results))
		if len(results) == 0:
			session["username"] = username
			taken = 0 
			usersTable.insert(entry)
			return redirect("/home")
			# TURN INTO LIST WHEN IT IS DONE
		else:
			taken = 1
			return render_template ("register.html", taken = taken)


@app.route('/login', methods = ["get" , "post"])
def login():
	if request.method == "GET":
		return render_template ("login.html")
	else:

		usersTable = db["users"]
		print (list(usersTable.find(username="omar@1")))
		form = request.form
		username= form["username"]
		password= form["password"]
		nameToCheck = username
		results = len(list(usersTable.find(username = nameToCheck, password=password)))
		if results > 0:
			login=2
			session["username"] = username
			print('sucessful login')
			return redirect('/home')
		else:
			login=0
			return render_template("login.html" , login=login)

@app.route('/logout')
def logout():
	if 'username' in session:
		logout = True
		session.pop('username', None)
		return render_template("login.html", logout=logout)
	else:
		return redirect("/home")


if __name__ == "__main__":
    app.run(port=5000)











