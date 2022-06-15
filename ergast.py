# Getting data using Ergast API

import json
import requests
from pprint import pprint

from dateutil import tz
from dateutil.tz import gettz
from datetime import datetime
from datetime import timezone

TZ_UTC = tz.gettz('UTC')
TZ_IN = tz.gettz('Asia/Kolkata')

url = requests.get('http://ergast.com/api/f1/current.json')
jsonData = url.text
data = json.loads(jsonData)
# pprint(data['MRData']['RaceTable']['Races'])

raceData = data['MRData']['RaceTable']['Races']

normalRaceWeekend = ['FirstPractice',
                     'SecondPractice', 'ThirdPractice', 'Qualifying']
sprintWeekend = ['FirstPractice', 'Qualifying', 'SecondPractice', 'Sprint']


def nextRace():
    i = 0
    for i in range(len(raceData)):
        date = data['MRData']['RaceTable']['Races'][i]['date']
        time = data['MRData']['RaceTable']['Races'][i]['time']
        dtStr = date + ' ' + time
        raceTimeUTC = datetime.strptime(dtStr, '%Y-%m-%d %H:%M:%SZ')
        timeNow = datetime.now(None)
        raceName = data['MRData']['RaceTable']['Races'][i]['raceName']
        if (raceTimeUTC > timeNow):
            print(f'Next Race is {raceName}')
            break
    return i+1


def nextEvent(raceNumber):
    raceNumber = raceNumber - 1
    timeNow = datetime.now(None)
    dateFP1 = data['MRData']['RaceTable']['Races'][raceNumber]['FirstPractice']['date']
    timeFP1 = data['MRData']['RaceTable']['Races'][raceNumber]['FirstPractice']['time']
    dtStrFP1 = dateFP1 + ' ' + timeFP1
    FP1_UTC = datetime.strptime(dtStrFP1, '%Y-%m-%d %H:%M:%SZ')

    dateFP2 = data['MRData']['RaceTable']['Races'][raceNumber]['SecondPractice']['date']
    timeFP2 = data['MRData']['RaceTable']['Races'][raceNumber]['SecondPractice']['time']
    dtStrFP2 = dateFP2 + ' ' + timeFP2
    FP2_UTC = datetime.strptime(dtStrFP2, '%Y-%m-%d %H:%M:%SZ')

    dateFP3 = data['MRData']['RaceTable']['Races'][raceNumber]['ThirdPractice']['date']
    timeFP3 = data['MRData']['RaceTable']['Races'][raceNumber]['ThirdPractice']['time']
    dtStrFP3 = dateFP3 + ' ' + timeFP3
    FP3_UTC = datetime.strptime(dtStrFP3, '%Y-%m-%d %H:%M:%SZ')

    dateQuali = data['MRData']['RaceTable']['Races'][raceNumber]['Qualifying']['date']
    timeQuali = data['MRData']['RaceTable']['Races'][raceNumber]['Qualifying']['time']
    dtStrQuali = dateQuali + ' ' + timeQuali
    Quali_UTC = datetime.strptime(dtStrQuali, '%Y-%m-%d %H:%M:%SZ')

    listOfEvents = [Quali_UTC, FP3_UTC, FP2_UTC, FP1_UTC]
    print(min(listOfEvents, key=lambda x: (x < timeNow, abs(x-timeNow))))


nextEvent(nextRace())
