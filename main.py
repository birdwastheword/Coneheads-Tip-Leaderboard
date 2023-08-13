import http.client
import json
import os
import urllib.parse
import base64
import datetime
from collections import defaultdict
import csv

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
    'User-Agent': f'avatar_bot_reader/0.1 by {username}',
    'Authorization': f'Bearer {jwt}'
}

# Process a batch of avatar bot comments.
totals = defaultdict(lambda:0,{})
biggest = ("", "", 0)

filename = f"runs/{yesterday.date()}/tips.csv"
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[0] == 'utc':
            #skip header
            day_of_tips = {}
        else:
            fromUser = row[1]
            toUser = row[2]
            amount = int(row[3])
            totals[fromUser] += amount
            if(amount >= biggest[2]):
                biggest = (fromUser, toUser, amount)

# Create reddit post output
totals = (dict(sorted(totals.items(), key=lambda item: -item[1])))
first = list(totals.items())[0]

rank = 0
comment = f"\r\nSince the official tipping leaderboard is still under construction I created a tipping leaderboard for just a single day. " \
          f"Congratulation to {first[0]} tipping {'{:,}'.format(first[1])} put you in the #1 spot. The biggest tip was from {biggest[0]} tipping {'{:,}'.format(biggest[2])} to {biggest[1]}\r\n" \
          "\r\nRank | Username | Totals Tips\r\n:-|:-|-:\r\n"
for name, total in totals.items():
  rank += 1
  comment += f"{rank} | {name.removeprefix(' /u/')} | {'{:,}'.format(total)}\r\n"

comment += f"\r\nThis day is defined starting at {yesterday.date()} 00:00 UTC and ending at {datetime.datetime.now().date()} 00:00 UTC.  \r\n" \
           f"The code generating this leaderboard is available for review here: https://github.com/birdwastheword/Coneheads-Tip-Leaderboard"
print(comment)

title=f"Daily Tipping Leaderboard {yesterday.strftime('%B %-d')} (Unofficial)"
payload = f'sr=ConeHeads&kind=self&title={urllib.parse.quote_plus(title)}&flair_id=d5c93210-4062-11ed-8995-3222414e6f3b&text={urllib.parse.quote_plus(comment)}'

print(title)
#conn.request("POST", "/api/submit", payload, headers)
#print(conn.getresponse().read().decode("utf-8"))
