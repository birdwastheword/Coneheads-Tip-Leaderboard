# Coneheads Tip Leaderboard
Scripts to create a daily leaderboard based on tips processed by https://www.reddit.com/user/avatarbot/comments

# main.py
This script will run daily [action](.github/workflows/cron.yml) at `00:15 UTC` and create a daily leaderboard for the previous day.  
After the leaderboard is created a post will be submitted to https://www.reddit.com/r/ConeHeads.

# download_comments.py
This script will run [action](.github/workflows/download_comments.yml) every 10 minutes and save comments data for future use.  
In order to be able to create overview for multiple day this script will save all tips of one in in `runs/yyyy-dd-mm/tips.csv`  
