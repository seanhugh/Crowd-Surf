import csv

from flask import redirect, render_template, request, session, url_for
from functools import wraps

from cs50sql import SQL as SQL
import datetime
from scalpyr import Scalpyr
seatgeek = Scalpyr()

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///tickets.db")

# Logs the current price data (ave, low, high, volume) for concert in table data (only call this on concerts that haven't happened)
def logData(id):
	try:
		# Searching for concerts ranked from most to least popular.... added in using a name to do it
		request_args = {"id":id}
		events = seatgeek.get_events(request_args)

		# Parse through dictionary to get prices
		data = events['events'][0]['stats']
		avPrice = data["average_price"]
		loPrice = data["lowest_price"]
		hiPrice = data["highest_price"]
		volume = data["listing_count"]
		social = "0"

		# Log what happened in the output file
		print("Added data for concert: " + id + " at time " + str(datetime.datetime.now()))

		# Add to Database (which table?)
		db.execute("INSERT INTO data (id,loPrice,avPrice,hiPrice,volume,social,datetime) VALUES (:id,:loPrice,:avPrice,:hiPrice,:volume,:social,:datetime)", id = id, loPrice=loPrice, avPrice=avPrice, hiPrice=hiPrice, volume=volume, social=social, datetime = str(datetime.datetime.now()))

	except ValueError:
		print("Error logging concert id: " + str(id) + "at time " + str(datetime.datetime.now()))

# Takes concert ID as parameter and adds the concert ID and end data of concert to table concerts
def addConcert(id):
	try:
		# Getting Datetime of concert and verifying that it exists
		request_args = {"id":id}
		events = seatgeek.get_events(request_args)

		# Verify that concert exists AND is not already in the database

		# Get Date of concert
		date = events['events'][0]['datetime_utc']

		# Add to concerts table in database
		
		db.execute("INSERT INTO concerts (id,end_date) VALUES (:id,:datetime)", id = id, datetime = date)

	except ValueError:
		# Return an error??
		print("Error Adding Concert")

def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

def concerts2Track():
	x = db.execute("SELECT * FROM concerts WHERE end_date > date('now')");
	return x











# # Searching for concerts ranked from most to least popular.... added in using a name to do it
# # request_args = {"type": "concert", "performers.slug": "billy-joel"}
# # events = seatgeek.get_events(request_args)
# # print events

# # Returns all events with the certain catch fraze.... will be awesome to use for the search feature
# request_args = "tiesto"
# events = seatgeek.search(request_args)
# print events