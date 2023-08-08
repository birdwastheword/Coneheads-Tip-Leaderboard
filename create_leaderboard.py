from collections import defaultdict
import os
import csv
import datetime

totals = defaultdict(lambda:0,{})

def process(filename):
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        #skip header
        line_count += 1
      else:
        fromUser = row[1]
        amount = int(row[3])
        line_count += 1
        totals[fromUser] += amount
  print(f'Processed    {line_count}    lines from {filename}.')

directory = os.fsencode("runs")
for file in os.listdir(directory):
  filename = f"runs/{os.fsdecode(file)}/tips.csv"
  process(filename)

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
