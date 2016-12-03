from flask import Flask, flash, redirect, render_template, request, session, url_for, json
from helpers import *
app = Flask(__name__)

# testing asdas
# HOMEPAGE
@app.route("/")
def index():
	listData = getAutocompleteData()
	print listData
	return render_template("index.html", autocompleteData = json.dumps(listData))

# CONCERT PAGE
@app.route('/all')
def all():
	return render_template("allConcert.html")

# ADD CONCERT
@app.route('/add')
def add():
	return render_template("addConcert.html")

# CONCERT PAGE
@app.route('/concert/<path:path>')
def catch_all(path):
	if isConcert(path):
		concertName = getConcertInfo(path)[0]['name']
		return render_template("page.html", concertName = concertName)
	else:
		return 'ERROR 404 CONCERT NOT FOUND'


if __name__ == "__main__":
    app.run()