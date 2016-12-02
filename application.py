from flask import Flask, flash, redirect, render_template, request, session, url_for
from helpers import *
app = Flask(__name__)

# HOMEPAGE
@app.route("/")
def hello():
    return render_template("index.html", title="deeez")

# CONCERT PAGE
@app.route('/<path:path>')
def catch_all(path):
	if isConcert(path):
		return render_template("concert.html")
	else:
		return 'ERROR 404 CONCERT NOT FOUND'
    

# def static_proxy(path):
#   # send_static_file will guess the correct MIME type
#   # print 'hey'
#   # return app.send_static_file(path)


if __name__ == "__main__":
    app.run()