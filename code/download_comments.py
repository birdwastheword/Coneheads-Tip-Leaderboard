import http.client
import json
import os
import datetime
import re
import csv
import reddit_oauth
import sys

#Set up
collect_day = datetime.datetime.now()
if len(sys.argv) == 2 and sys.argv[1] == 'yesterday':
  collect_day = datetime.datetime.now() - datetime.timedelta(days = 1)

# Get avatar bot comments
jwt = reddit_oauth.jwt()
conn = http.client.HTTPSConnection("oauth.reddit.com")
payload = ''
headers = {
  'User-Agent': f'avatar_bot_reader/0.1 by {reddit_oauth.username}',
  'Authorization': f'Bearer {jwt}'
}

# Read the current list of tips, this is needed when the amout of tips in one day exceeds the api limit
day_of_tips = {}

filename = f"runs/{collect_day.date()}/tips.csv"
if os.path.exists(filename):
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      if row[0] != 'utc': #skip header
        day_of_tips[(row[0], row[1].removeprefix(' '))] = (row[2].removeprefix(' '), int(row[3].removeprefix(' ')), row[4].removeprefix(' '), row[5].removeprefix(' '))

# Process batches of avatarbot comments
def process(data):
  for comment in data["children"]:
    utc = datetime.datetime.utcfromtimestamp(comment["data"]["created_utc"])

    #Save comment tip in CSV
    global tips_csv
    res = re.match("(/u/[\w-]+)\W(has)\W(tipped)\W(/u/[\w-]+)\W(\d+)\W(Bitcone)", comment["data"]["body"])
    sub = comment["data"]["subreddit_name_prefixed"]
    if(res and (utc.date() == collect_day.date())) :
      fromUser = (res.groups()[0])
      toUser = (res.groups()[3])
      amount = int(res.groups()[4])
      currency = (res.groups()[5])
      day_of_tips[(f"{utc}", fromUser)] = (toUser, amount, currency, sub)

# Download batches of avatarbot comments.
after = ""
while after != None :
  conn.request("GET", f"/user/avatarbot/comments?limit=1000&after={after}", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data = json.loads(data.decode("utf-8"))
  process(data["data"])
  after = (data["data"]["after"])

# Collect all JSON batches in one file
day_of_tips = (dict(sorted(day_of_tips.items(), key=lambda item: item[0])))
tips_csv = "utc, from_user, to_user, amount, currency, sub_reddit\r\n"
for (utc, fromUser), (toUser, amount, currency, sub) in day_of_tips.items():
  tips_csv += (f"{utc}, {fromUser}, {toUser}, {amount}, {currency}, {sub}\r\n")

#Save the comment tip to CSV file
filename = f"runs/{collect_day.date()}/tips.csv"
os.makedirs(os.path.dirname(filename), exist_ok=True)
f = open(filename, "w")
f.write(tips_csv)
print(f"written to {f.name}")
f.close()
