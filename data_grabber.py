# THIS FILE RUNS CONSTANTLY. IT GETS DATA FOR EVERY CONCERT THAT HAS NOT YET
# OCCURED. IT DOES THIS OVER A 30 MINUTE PERIOD.
from helpers import *
import time

# the following while loop will grab data for each of the concert at 30 minute intervals 
while(True):
	try:
		#first I will go and get a list of all the IDs that I have to track:
		ids_to_track = concerts2Track()

		# This updates each concert over a span of 30 minutes
		time_to_wait = (30/len(ids_to_track))*60

		for i in ids_to_track:
			# Try here to stop crashing in case of one bad concert
			try:
				# Get current data for said concert
				logData(i['id'])

				# Wait the designated amoint of time
				time.sleep(time_to_wait)
			except:
				print("We failed to get data on concert: " + i)
	except:
	     pass