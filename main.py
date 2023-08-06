import http.client
import json
import os
import urllib.parse
import base64
import re
import datetime

# Set up env
client_id = os.environ["CLIENT_ID"]
cliend_secret = os.environ["CLIENT_SECRET"]
username = os.environ["REDDIT_NAME"]
password = os.environ["PASSWORD"]
token = base64.b64encode(f"{client_id}:{cliend_secret}".encode('utf-8')).decode("ascii")
yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)

# Obtain JTW
conn = http.client.HTTPSConnection("www.reddit.com")
payload = f'grant_type=password&username={urllib.parse.quote_plus(username)}&password={urllib.parse.quote_plus(password)}'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': f'avatar_bot_reader/0.1 by {username}',
  'Authorization': f'Basic {token}',
}
conn.request("POST", "/api/v1/access_token", payload, headers)
res = conn.getresponse()
data = res.read().decode("utf-8")
jwt = json.loads(data)["access_token"]

print(f"jwt obtained: {jwt}")

# Get avatar bot comments
conn = http.client.HTTPSConnection("oauth.reddit.com")
payload = ''
headers = {
  'User-Agent': 'avatar_bot_reader/0.1 by birdwastheword',
  'Authorization': f'Bearer {jwt}'
}

# Process a batch of avatar bot comments.
def process(data):
  for comment in data["children"]:
    res = re.match("(/u/\w+)\W(has)\W(tipped)\W(/u/\w+)\W(\d+)\W(Bitcone)", comment["data"]["body"])
    utc = datetime.datetime.utcfromtimestamp(comment["data"]["created_utc"])
    sub = comment["data"]["subreddit_name_prefixed"]

    if(res and (utc.date() == yesterday.date())) :
      fromUser = (res.groups()[0])
      toUser = (res.groups()[3])
      amount = int(res.groups()[4])
      currency = (res.groups()[5])
      print(f"{utc}, {fromUser}, {toUser}, {amount}, {currency}, {sub}")

# Download batches of avatarbot comments.
after = ""
while after != None :
  conn.request("GET", f"/user/avatarbot/comments?limit=100&after={after}", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data = json.loads(data.decode("utf-8"))
  process(data["data"])
  after = (data["data"]["after"])
