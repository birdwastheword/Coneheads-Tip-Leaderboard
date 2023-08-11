# Coneheads Tip Leaderboard
Scripts to create leaderboards based on tips processed by https://www.reddit.com/user/avatarbot/comments

# Genaral note on CRON tiggers in `github/workflows`
Unfortunatly the CRON triggers in Github actions are on a best effort basis and could experience quite some delay.  

# main.py
This script will run daily [action](.github/workflows/cron.yml) at `00:15 UTC` and create a daily leaderboard for the previous day.  
After the leaderboard is created a post will be submitted to https://www.reddit.com/r/ConeHeads.

# download_comments.py
This script will run [action](.github/workflows/download_comments.yml) every 10 minutes and saves tip comment data for future use.  
In order to be able to create overview for multiple days this script will save all tips of one day in `runs/yyyy-dd-mm/tips.csv`.  
It will also run one final time during the creation of the daily leaderboard, in order to capture all tips at the end of the previous day.

# create_leaderboard.py
This script will run [action](.github/workflows/download_comments.yml) every 10 minutes after the latest tips are inserted in `runs/today/tips.csv`.  
This script parses all `tips.csv` files form the `runs` folders and compiles the total leaderboard in `leaderboard-total.md`.  
I will also gather all tips 1,000,000 and above and add them into the [Hall of Fame](hall-of-fame.md)

# exclude_tip.py
Sometimes a user uses the `!tip` command to pay for an avatar or something else. Since that is not really a tip we should not count them towards the leaderboard. By adding the timestamp and username this tips will be excluded. This list of excludes can also be used to exclude tips that do not qualify as "Fair play". 
