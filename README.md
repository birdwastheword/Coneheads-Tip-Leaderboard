# Coneheads Tip Leaderboard
Scripts to create leaderboards based on tips processed by https://www.reddit.com/user/avatarbot/comments

### General note on CRON tiggers in `github/workflows`
Unfortunatly the CRON triggers in Github actions are on a best effort basis and could experience quite some delay.  

## Scheduled Actions
### Every 10 Minutes Process Tips
This [action](.github/workflows/download_comments.yml) will run every 10 minutes.
It wil perfrom two steps
1. Run `download_comments`
2. Run `create_leaderboard.py`

### Dialy Post Leaderboard
This [action](.github/workflows/post_leaderboard.yml) will run run at the end of the day at `00:15 UTC`.
It wil perfrom two steps
1. Run `download_comments` for `yesterday`
2. Run `create_leaderboard.py`

## Python Scripts
### code/download_comments.py
In order to be able to create overview for multiple days this script will save all tips of one day in `runs/yyyy-dd-mm/tips.csv`.  
It will merge data already in the csv with newly found tips to make sure no data is lost when tips per day exceeds the API limit.

### code/post_leaderboard.py
Create a daily leaderboard for the previous day.  
After the leaderboard is created a post will be submitted to https://www.reddit.com/r/ConeHeads.

### code/create_leaderboard.py
This script parses all `tips.csv` files form the `runs` folders and compiles the total leaderboard in [Leaderboard](leaderboard-total.md).  
It will also gather all tips 1,000,000 and above and add them into the [Hall of Fame](hall-of-fame.md).  
The same data will be exported in JSON format to [web folder](web).  
[Leaderboard]([Leaderboard]() and [Hall of Fame](https://birdwastheword.github.io/Coneheads-Tip-Leaderboard/web/leaderboard.json) ) and [Hall of Fame](https://birdwastheword.github.io/Coneheads-Tip-Leaderboard/web/cone-of-fame.json) is available here.  

### exclude_tip.py (mostly suspended)
Sometimes a user uses the `!tip` command to pay for an avatar or something else. Since that is not really a tip we should not count them towards the leaderboard. By adding the timestamp and username this tips will be excluded. This list of excludes can also be used to exclude tips that do not qualify as "Fair play". 
