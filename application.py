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
    # GET LIST OF ALL UPCOMING CONCERTS
    concerts = concerts2Track()

    print concerts

    #RETURN TEMPLATE WITH LIST
    return render_template("allConcert.html", concerts=concerts)

# ADD CONCERT
@app.route('/add', methods=["GET", "POST"])
def add():
	# if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

    	# ensure symbol and shares were submitted
        if request.form.get("addConcertForm"):
            
            #set symbol variable
            symbol=request.form.get("addConcertForm")

            # Send Query
            concerts = queryConcerts(symbol);

            # Return the template with concert results
            return render_template("addConcert.html", concerts=concerts)

        # ensure symbol and shares were submitted
        if request.form.get("addButton"):
            
            # #set symbol variable
            id=request.form.get("addButton")

            # add Concert to Database
            addConcert(id)

            # Log the Data for it
            logData(id)

            # Return the template with concert results
            return redirect("/concert/" + id)

        else:
            return "NOTHING IN THE SEARCH"

        
        
        # look too see if user owns any of this stock
        # stocks = db.execute("SELECT * FROM portfolio WHERE id = :id AND symbol LIKE :symbol", id=session["user_id"], symbol=symbol)
        
    else:
		return render_template("addConcert.html", concerts=[])

# CONCERT PAGE
@app.route('/concert/<path:path>')
def catch_all(path):
    if isConcert(path):
        priceData = getChartdata(path)
        concertName = getConcertInfo(path)[0]['name']
        print json.dumps(priceData)
        return render_template("page.html", concertName = concertName, priceData = json.dumps(priceData))
    else:
		return 'ERROR 404 CONCERT NOT FOUND'


if __name__ == "__main__":
    app.run(threaded=True)