# Getting data using Ergast API

import json
import requests
from pprint import pprint

from dateutil import tz
from dateutil.tz import gettz
from datetime import datetime

TZ_UTC = tz.gettz('UTC')
TZ_IN = tz.gettz('Asia/Kolkata')

url = requests.get('http://ergast.com/api/f1/current.json')
jsonData = url.text
data = json.loads(jsonData)
pprint(data['MRData']['RaceTable']['Races'])

date = data['MRData']['RaceTable']['Races'][0]['date']
time = data['MRData']['RaceTable']['Races'][0]['time']
dtStr = date + ' ' + time
dtUTC = datetime.strptime(dtStr, '%Y-%m-%d %H:%M:%SZ')
utc = dtUTC.replace(tzinfo=TZ_UTC)
local = utc.astimezone(TZ_IN)
print(local.isoformat(timespec='seconds'))

raceData = data['MRData']['RaceTable']['Races']


def nextRace():
    for i in range(len(raceData)):      # change to while loop. while dtDiff is -ve
        date = data['MRData']['RaceTable']['Races'][i]['date']
        time = data['MRData']['RaceTable']['Races'][i]['time']
        dtStr = date + ' ' + time
        dtDiff = datetime.strptime(
            dtStr, '%Y-%m-%d %H:%M:%SZ') - datetime.now(TZ_UTC)
        if (dtDiff > 0):
            return i+1        # Race number
