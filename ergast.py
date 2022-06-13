# Getting data using Ergast API

import json
import requests
from pprint import pprint

from dateutil import tz
from dateutil.tz import gettz
from datetime import datetime

url = requests.get('http://ergast.com/api/f1/current.json')
jsonData = url.text
data = json.loads(jsonData)
pprint(data['MRData']['RaceTable']['Races'])

date = data['MRData']['RaceTable']['Races'][0]['date']
time = data['MRData']['RaceTable']['Races'][0]['time']
dtStr = date + ' ' + time
dtUTC = datetime.strptime(dtStr, '%Y-%m-%d %H:%M:%SZ')
utc = dtUTC.replace(tzinfo=tz.gettz('UTC'))
local = utc.astimezone(tz.gettz('Asia/Kolkata'))
print(local.isoformat(timespec='seconds'))
