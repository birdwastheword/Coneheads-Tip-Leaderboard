# Coneheads Tip Leaderboard
Scripts to create a daily leaderboard based on tips processed by https://www.reddit.com/user/avatarbot/comments

# Genaral note on CRON tiggers in `github/workflows`
Unfortunatly the CRON trigger in Github actions are on a best effort basis and could experience quite some delay.  

# main.py
This script will run daily [action](.github/workflows/cron.yml) at `00:15 UTC` and create a daily leaderboard for the previous day.  
After the leaderboard is created a post will be submitted to https://www.reddit.com/r/ConeHeads.

# download_comments.py
This script will run [action](.github/workflows/download_comments.yml) every 10 minutes and save comments data for future use.  
In order to be able to create overview for multiple day this script will save all tips of one in in `runs/yyyy-dd-mm/tips.csv`.  
It will also run one final time during the creation of the daily leaderboard, in order to capture all tips at the end of the last day.

# create_leaderboard.py
This script will run [action](.github/workflows/download_comments.yml) every 10 minutes after the latest tips are inserted in `runs/today/tips.csv`.  
This script parses all `tips.csv` files form the `runs` folders and compiles the total leaderboard in `leaderboard-total.md`
