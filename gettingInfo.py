# # RUN IN PYTHON 2
import requests
import base64
import pprint

## Enter user's API key, secret, and Stubhub login
app_token = '_IhSxoGHKdGzUN0L0az_rfRsSgMa'
consumer_key = "_mXxw8ljvYhQNCYOHrtuCaJ5wdga"
consumer_secret = "kKPjT7wlSJTxXsZ5k_QMbNGJuoca"
stubhub_username = "seanthushan@gmail.com"
stubhub_password = "FinalProject1234!"

## LOG THE USER INTO THE WEBSITE BY ENCRYPTING

combo = consumer_key + ':' + consumer_secret
basic_authorization_token = base64.b64encode(combo)

url = 'https://api.stubhub.com/login'
headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'Authorization':'Basic '+basic_authorization_token,}
body = {
        'grant_type':'password',
        'username':stubhub_username,
        'password':stubhub_password,
        'scope':'PRODUCTION'}

r = requests.post(url, headers=headers, data=body)
print(r)
print(r.text)

token_respoonse = r.json()
access_token = token_respoonse['access_token']
user_GUID = r.headers['X-StubHub-User-GUID']

# NOW THAT THE USER IS LOGGED IN, BEGIN ACCESSING THE DATA

inventory_url = 'https://api.stubhub.com/search/inventory/v1/sectionsummary?eventID=9705184'
eventid = '9705184'
data = {'eventid':eventid}
headers['Authorization'] = 'Bearer ' + access_token
headers['Accept'] = 'application/json'
headers['Accept-Encoding'] = 'application/json'

inventory = requests.get(inventory_url, headers=headers)

print inventory.text
print "d"

# inv = inventory.json()
# pprint.pprint(inv['listing'])