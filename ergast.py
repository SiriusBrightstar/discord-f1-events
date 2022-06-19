# Getting data using Ergast API

import json
import requests
from pprint import pprint

import pytz
from datetime import datetime, tzinfo

TZ_UTC = pytz.timezone('UTC')
TZ_IN = pytz.timezone('Asia/Kolkata')

url = requests.get('http://ergast.com/api/f1/current.json')
jsonData = url.text
data = json.loads(jsonData)
# pprint(data['MRData']['RaceTable']['Races'])

raceData = data['MRData']['RaceTable']['Races']

normalRaceWeekend = ['FirstPractice',
                     'SecondPractice', 'ThirdPractice', 'Qualifying', 'Race']
sprintWeekend = ['FirstPractice', 'Qualifying', 'SecondPractice', 'Sprint', 'Race']


def nextRace():
    i = 0
    for i in range(len(raceData)):
        date = data['MRData']['RaceTable']['Races'][i]['date']
        time = data['MRData']['RaceTable']['Races'][i]['time']
        dtStr = date + ' ' + time
        raceTimeUTC = datetime.strptime(dtStr, '%Y-%m-%d %H:%M:%SZ')
        raceTimeUTC = raceTimeUTC.replace(tzinfo=TZ_UTC)
        timeNow = datetime.now(TZ_UTC)
        raceName = data['MRData']['RaceTable']['Races'][i]['raceName']
        if (raceTimeUTC > timeNow):
            print(f'Next Race is {raceName}')
            break
    return i+1


def nextEvent(raceNumber):
    raceNumber = raceNumber - 1
    timeNow = datetime.now(TZ_UTC)
    dateFP1 = data['MRData']['RaceTable']['Races'][raceNumber]['FirstPractice']['date']
    timeFP1 = data['MRData']['RaceTable']['Races'][raceNumber]['FirstPractice']['time']
    dtStrFP1 = dateFP1 + ' ' + timeFP1
    FP1_UTC = datetime.strptime(dtStrFP1, '%Y-%m-%d %H:%M:%SZ')
    FP1_UTC = FP1_UTC.replace(tzinfo=TZ_UTC)

    dateFP2 = data['MRData']['RaceTable']['Races'][raceNumber]['SecondPractice']['date']
    timeFP2 = data['MRData']['RaceTable']['Races'][raceNumber]['SecondPractice']['time']
    dtStrFP2 = dateFP2 + ' ' + timeFP2
    FP2_UTC = datetime.strptime(dtStrFP2, '%Y-%m-%d %H:%M:%SZ')
    FP2_UTC = FP2_UTC.replace(tzinfo=TZ_UTC)

    dateQuali = data['MRData']['RaceTable']['Races'][raceNumber]['Qualifying']['date']
    timeQuali = data['MRData']['RaceTable']['Races'][raceNumber]['Qualifying']['time']
    dtStrQuali = dateQuali + ' ' + timeQuali
    Quali_UTC = datetime.strptime(dtStrQuali, '%Y-%m-%d %H:%M:%SZ')
    Quali_UTC = Quali_UTC.replace(tzinfo=TZ_UTC)

    dateRace = data['MRData']['RaceTable']['Races'][raceNumber]['date']
    timeRace = data['MRData']['RaceTable']['Races'][raceNumber]['time']
    dtStrRace = dateRace + ' ' + timeRace
    Race_UTC = datetime.strptime(dtStrRace, '%Y-%m-%d %H:%M:%SZ')
    Race_UTC = Race_UTC.replace(tzinfo=TZ_UTC)

    if 'ThirdPractice' in data['MRData']['RaceTable']['Races'][raceNumber]:
        dateFP3 = data['MRData']['RaceTable']['Races'][raceNumber]['ThirdPractice']['date']
        timeFP3 = data['MRData']['RaceTable']['Races'][raceNumber]['ThirdPractice']['time']
        dtStrFP3 = dateFP3 + ' ' + timeFP3
        FP3_UTC = datetime.strptime(dtStrFP3, '%Y-%m-%d %H:%M:%SZ')
        FP3_UTC = FP3_UTC.replace(tzinfo=TZ_UTC)
        listOfEvents = [FP1_UTC, FP2_UTC, FP3_UTC, Quali_UTC, Race_UTC]
        nextSessionTime = min([date for date in listOfEvents if date >= timeNow])
        nextSessionName = listOfEvents.index(nextSessionTime)
        sessionTimeLocal = nextSessionTime.replace(
            tzinfo=TZ_UTC).astimezone(TZ_IN).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        print(
            f'Session: {normalRaceWeekend[nextSessionName]} at {sessionTimeLocal}')
    else:
        dateSprint = data['MRData']['RaceTable']['Races'][raceNumber]['Sprint']['date']
        timeSprint = data['MRData']['RaceTable']['Races'][raceNumber]['Sprint']['time']
        dtStrSprint = dateSprint + ' ' + timeSprint
        Sprint_UTC = datetime.strptime(dtStrSprint, '%Y-%m-%d %H:%M:%SZ')
        Sprint_UTC = Sprint_UTC.replace(tzinfo=TZ_UTC)
        listOfEvents = [FP1_UTC, Quali_UTC, FP2_UTC, Sprint_UTC, Race_UTC]
        nextSessionTime = min([date for date in listOfEvents if date >= timeNow])
        nextSessionName = listOfEvents.index(nextSessionTime)
        sessionTimeLocal = nextSessionTime.replace(
            tzinfo=TZ_IN).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        print(
            f'Session: {sprintWeekend[nextSessionName]} at {sessionTimeLocal}')


nextEvent(nextRace())
