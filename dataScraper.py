from scalpyr import Scalpyr
seatgeek = Scalpyr()

# Searching for concerts ranked from most to least popular.... added in using a name to do it
# request_args = {"type": "concert", "performers.slug": "billy-joel"}
# events = seatgeek.get_events(request_args)
# print events

# Returns all events with the certain catch fraze.... will be awesome to use for the search feature
request_args = "tiesto"
events = seatgeek.search(request_args)
print events