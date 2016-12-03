from flask import Flask, flash, redirect, render_template, request, session, url_for, json
from helpers import *
app = Flask(__name__)

# testing asdas
# HOMEPAGE
@app.route("/")
def index():
	listData = ["one", "two", "three", "four"]
	return render_template("index.html", autocompleteData = json.dumps(listData))

# CONCERT PAGE
@app.route('/<path:path>')
def catch_all(path):
	if isConcert(path):
		concertName = getConcertInfo(path)[0]['name']
		return render_template("concert.html", concertName = concertName)
	else:
		return 'ERROR 404 CONCERT NOT FOUND'
    

# def static_proxy(path):
#   # send_static_file will guess the correct MIME type
#   # print 'hey'
#   # return app.send_static_file(path)


if __name__ == "__main__":
    app.run()