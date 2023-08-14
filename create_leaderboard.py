from collections import defaultdict
import os
import csv
import datetime
import exclude_tip
import json

totals = defaultdict(lambda:0,{})
hall_of_fame = []

def process(filename):
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        #skip header
        line_count += 1
      elif (row[0], row[1].removeprefix(' ')) in exclude_tip.exclude_tip :
        #skip comment
        line_count += 1
      else:
        utc = row[0]
        fromUser = row[1]
        toUser = row[2]
        amount = int(row[3])
        line_count += 1
        totals[fromUser] += amount
        if amount >= 1000000:
          global hall_of_fame
          hall_of_fame.append((utc, fromUser, toUser, amount))
  print(f'Processed    {line_count}    lines from {filename}.')

directory = os.fsencode("runs")
for file in os.listdir(directory):
  filename = f"runs/{os.fsdecode(file)}/tips.csv"
  process(filename)

#Create leaderboard
totals = (dict(sorted(totals.items(), key=lambda item: -item[1])))
rank = 0
leaderboard = f"Last updated: {datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')} UTC  \r\nRank | Username | Totals Tips\r\n:-|:-|-:\r\n"
for name, total in totals.items():
  rank += 1
  leaderboard += f"{rank} | {name.removeprefix(' /u/')} | {'{:,}'.format(total)}\r\n"

filename = "leaderboard-total.md"
f = open(filename, "w")
f.write(leaderboard)
print(f"written to {f.name}")
f.close()

#Create Hall of Fame
hall_sorted = sorted(hall_of_fame, key=lambda t: (-t[3], t[0]))
rank = 0
hall_text = "Tips Hall of Fame:\r\nRank | Date | Username | Totals Tips | to User\r\n:-|:-|:-|-:|:-\r\n"
for (date, fromUser, toUser, amount) in hall_sorted:
  rank += 1
  hall_text += f"{rank} | {date} | {fromUser.removeprefix(' /u/')} | {'{:,}'.format(amount)}| {toUser.removeprefix(' /u/')}\r\n"

hall_text += "\r\nTips over 1,000,000 will be eligible for the Hall of Fame\r\n"

filename = "hall-of-fame.md"
f = open(filename, "w")
f.write(hall_text)
print(f"written to {f.name}")
f.close()

#Create Cone of Fame JSON
hall_json = []
rank = 0
for (date, fromUser, toUser, amount) in hall_sorted:
  rank += 1
  hall_json += [{ "rank" : rank, "date" : date, "fromUser" : fromUser, "toUser" : toUser, "amount" : amount}]
with open('web/cone-of-fame.json', 'w') as f:
  json.dump(hall_json, f)
