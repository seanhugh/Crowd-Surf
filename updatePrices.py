import datetime
from scalpyr import Scalpyr
seatgeek = Scalpyr()

def logData(id):
	try:
        # Check to make sure concert has not yet occured. Remove if it has.

		# Searching for concerts ranked from most to least popular.... added in using a name to do it
		request_args = {"id":id}
		events = seatgeek.get_events(request_args)

		# Parse through dictionary to get prices
		data = events['events'][0]['stats']
		avPrice = data["average_price"]
		loPrice = data["lowest_price"]
		HiPrice = data["highest_price"]
		volume = data["listing_count"]

		# Get the current datetime
		time = datetime.datetime.now()

		# Add to Database (which table?)

	except ValueError:
		print("Error logging concert id: " + str(id) + "at time " + str(datetime.datetime.now()))


logData("3598217")