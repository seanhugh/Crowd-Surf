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
		description = ''
		date = events['events'][0]['datetime_utc']
		title = events['events'][0]['title']
		location = events['events'][0]['venue']['city']
		venue = events['events'][0]['venue']['name']

		# Add to concerts table in database
		db.execute("INSERT INTO concerts (id,datetime,name,description,location,venue,misc) VALUES (:id, :date, :title, :description, :location, :venue, :misc)", id=id,date=date,title=title,description=description,location=location,venue=venue,misc=description)
	
	except ValueError:
		# Return an error??
		print("Error Adding Concert")

# Returns the concerts that have not yet occured
def concerts2Track():
	x = db.execute("SELECT * FROM concerts WHERE datetime > date('now')");
	return x

# Returns the concerts that have not yet occured
def getPriceData(id):
	x = db.execute("SELECT * FROM data WHERE id LIKE :id", id=id);
	return x

def getChartdbdata(id):
	x = db.execute("SELECT datetime,loPrice,avPrice,hiPrice FROM data WHERE id LIKE :id", id=id);
	return x

# Returns the concerts that have not yet occured
def getConcertInfo(id):
	x = db.execute("SELECT * FROM concerts WHERE id LIKE :id", id=id);
	return x

def getinitialvolume(id):
	x = db.execute("SELECT volume FROM data ORDER BY :id ASC LIMIT 1", id=id);
	return x

def getminPricingData(id):
	x = db.execute("SELECT MAX(loPrice) FROM data WHERE id LIKE :id;", id=id);
	return x

def getminiminPricingData(id):
	x = db.execute("SELECT MIN(loPrice) FROM data WHERE id LIKE :id;", id=id);
	return x

# Returns if the given string is a concert ID
def isConcert(id):
	x = db.execute("SELECT * FROM concerts WHERE id LIKE :id", id=id);
	if (len(x) > 0):
		return 1
	else:
		return 0

def usd(y):
	return('${:,.2f}'.format(y))

def getAutocompleteData():
	x =concerts2Track()
	tempList = []
	for i in x:
		tempName = i['name']
		tempID = i['id']
		tempList.append({'id':tempID, 'label':tempName})
	return tempList

def getChartdata(id):
	x = getChartdbdata(id)
	tempList2 = []
	for i in x:
		tempTime = i['datetime']
		tempPrice = float(i['loPrice'])
		tempavPrice = float(i['avPrice'])
		temphiPrice = float(i['hiPrice'])
		tempList2.append([tempPrice, tempTime, tempavPrice, temphiPrice])
	return tempList2


def getminPricer(id):
	x = getminPricingData(id)
	for i in x:
		y = float(i['MAX(loPrice)'])
	return(usd(y))

def initvolume(id):
	x = getinitialvolume(id)
	for i in x:
		y = float(i['volume'])
	return(y)

def getminiminPricer(id):
	x = getminiminPricingData(id)
	for i in x:
		y = float(i['MIN(loPrice)'])
	return(usd(y))


def queryConcerts(key):
	# Returns all events with the certain catch fraze.... will be awesome to use for the search feature
	request_args = key
	events = seatgeek.search(request_args)
	return events


# # Searching for concerts ranked from most to least popular.... added in using a name to do it
# # request_args = {"type": "concert", "performers.slug": "billy-joel"}
# # events = seatgeek.get_events(request_args)
# # print events

