# Get raw data using:
# grep -F 'CustomGame' /var/log/syslog | grep 'created\|launched' > /tmp/game_create_launch_time
# Then pipe to this script

import sys
import datetime

months = {
'Jan':1,
'Feb':2,
'Mar': 3,
'Apr':4,
'May':5,
'Jun':6,
'Jul':7,
'Aug':8,
'Sep':9,
'Oct':10,
'Nov':11,
'Dec':12
}

games = {}

for line in sys.stdin.readlines():
  comps = line.split()
  month = months[comps[0]]
  day = int(comps[1])
  tm = [int(x) for x in comps[2].split(':')]
  game_id = comps[6]
  action = comps[-1]
  dt = datetime.datetime(year=2017, month=month, day=day, hour=tm[0], minute=tm[1], second=tm[2])
  game = games.get(game_id, {})
  game[action] = dt
  games[game_id] = game

for game_id, game_info in games.items():
  if 'created' in game_info and 'launched' in game_info:
    created = game_info['created']
    launched = game_info['launched']
    span = launched - created
    print("{};{};{};{}".format(game_id, created, launched, span))
