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
@app.route('/add', methods=["GET", "POST"])
def add():
	# if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

    	# ensure symbol and shares were submitted
        if not request.form.get("addConcertForm"):
            return "NOTHING IN THE SEARCH"
            
        #set symbol variable
        symbol=request.form.get("addConcertForm")

        # Send Query
        concerts = queryConcerts(symbol);

        return render_template("addConcert.html", concerts=concerts)
        
        # look too see if user owns any of this stock
        # stocks = db.execute("SELECT * FROM portfolio WHERE id = :id AND symbol LIKE :symbol", id=session["user_id"], symbol=symbol)
        
    else:
		return render_template("addConcert.html", concerts=[])

# CONCERT PAGE
@app.route('/concert/<path:path>')
def catch_all(path):
	if isConcert(path):
		concertName = getConcertInfo(path)[0]['name']
		return render_template("page.html", concertName = concertName)
	else:
		return 'ERROR 404 CONCERT NOT FOUND'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)