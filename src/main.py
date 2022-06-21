"""
Discord Sidebar bot to display the next F1 event

By SiriusBrightstar
"""

import json
import logging
import requests

import pytz
from datetime import datetime

import discord
from discord.ext import tasks

from auth import TOKEN, GUILD_ID, BOT_ID, LOCAL_TIMEZONE, STR_TIME_FORMAT

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s -> %(levelname)s: %(message)s\n-----', level=logging.INFO)

REFRESH_RATE = 30*60    # Refresh every 30 mins

client = discord.Client()


TZ_UTC = pytz.timezone('UTC')
TZ_IN = pytz.timezone(LOCAL_TIMEZONE)       # Change this to your Local Time

url = requests.get('http://ergast.com/api/f1/current.json')
jsonData = url.text
data = json.loads(jsonData)

raceData = data['MRData']['RaceTable']['Races']

normalRaceWeekend = ['FP1', 'FP2', 'FP3', 'Q', 'Race']
sprintWeekend = ['FP1', 'Q', 'FP2', 'S', 'Race']


def nextRace():
    i = 0
    for i in range(len(raceData)):
        date = raceData[i]['date']
        time = raceData[i]['time']
        dtStr = date + ' ' + time
        raceTimeUTC = datetime.strptime(dtStr, '%Y-%m-%d %H:%M:%SZ')
        raceTimeUTC = raceTimeUTC.replace(tzinfo=TZ_UTC)
        timeNow = datetime.now(TZ_UTC)
        raceName = raceData[i]['raceName'].replace(
            'Grand Prix', 'GP')
        if (raceTimeUTC > timeNow):
            print(f'Next Race is {raceName}')
            break
    return i+1  # Adding 1 to get race number


def nextEvent(raceNumber):
    raceNumber = raceNumber - 1     # Subtracting 1 as the list index starts from 0
    timeNow = datetime.now(TZ_UTC)

    raceName = raceData[raceNumber]['raceName'].replace(
        'Grand Prix', 'GP')

    dateFP1 = raceData[raceNumber]['FirstPractice']['date']
    timeFP1 = raceData[raceNumber]['FirstPractice']['time']
    dtStrFP1 = dateFP1 + ' ' + timeFP1
    FP1_UTC = datetime.strptime(dtStrFP1, '%Y-%m-%d %H:%M:%SZ')
    FP1_UTC = FP1_UTC.replace(tzinfo=TZ_UTC)

    dateFP2 = raceData[raceNumber]['SecondPractice']['date']
    timeFP2 = raceData[raceNumber]['SecondPractice']['time']
    dtStrFP2 = dateFP2 + ' ' + timeFP2
    FP2_UTC = datetime.strptime(dtStrFP2, '%Y-%m-%d %H:%M:%SZ')
    FP2_UTC = FP2_UTC.replace(tzinfo=TZ_UTC)

    dateQuali = raceData[raceNumber]['Qualifying']['date']
    timeQuali = raceData[raceNumber]['Qualifying']['time']
    dtStrQuali = dateQuali + ' ' + timeQuali
    Quali_UTC = datetime.strptime(dtStrQuali, '%Y-%m-%d %H:%M:%SZ')
    Quali_UTC = Quali_UTC.replace(tzinfo=TZ_UTC)

    dateRace = raceData[raceNumber]['date']
    timeRace = raceData[raceNumber]['time']
    dtStrRace = dateRace + ' ' + timeRace
    Race_UTC = datetime.strptime(dtStrRace, '%Y-%m-%d %H:%M:%SZ')
    Race_UTC = Race_UTC.replace(tzinfo=TZ_UTC)

    if 'ThirdPractice' in raceData[raceNumber]:
        dateFP3 = raceData[raceNumber]['ThirdPractice']['date']
        timeFP3 = raceData[raceNumber]['ThirdPractice']['time']
        dtStrFP3 = dateFP3 + ' ' + timeFP3
        FP3_UTC = datetime.strptime(dtStrFP3, '%Y-%m-%d %H:%M:%SZ')
        FP3_UTC = FP3_UTC.replace(tzinfo=TZ_UTC)
        listOfEvents = [FP1_UTC, FP2_UTC, FP3_UTC, Quali_UTC, Race_UTC]
        nextSessionTime = min(
            [date for date in listOfEvents if date >= timeNow])
        nextSessionName = normalRaceWeekend[listOfEvents.index(
            nextSessionTime)]
        sessionTimeLocal = nextSessionTime.replace(
            tzinfo=TZ_UTC).astimezone(TZ_IN).strftime(STR_TIME_FORMAT)
        logging.info(f'Session: {nextSessionName} at {sessionTimeLocal}')
    else:
        dateSprint = raceData[raceNumber]['Sprint']['date']
        timeSprint = raceData[raceNumber]['Sprint']['time']
        dtStrSprint = dateSprint + ' ' + timeSprint
        Sprint_UTC = datetime.strptime(dtStrSprint, '%Y-%m-%d %H:%M:%SZ')
        Sprint_UTC = Sprint_UTC.replace(tzinfo=TZ_UTC)
        listOfEvents = [FP1_UTC, Quali_UTC, FP2_UTC, Sprint_UTC, Race_UTC]
        nextSessionTime = min(
            [date for date in listOfEvents if date >= timeNow])
        nextSessionName = sprintWeekend[listOfEvents.index(nextSessionTime)]
        sessionTimeLocal = nextSessionTime.replace(
            tzinfo=TZ_IN).strftime(STR_TIME_FORMAT)
        logging.info(f'Session: {nextSessionName} at {sessionTimeLocal}')

    return [raceName, nextSessionName, sessionTimeLocal]


@tasks.loop(seconds=REFRESH_RATE)
async def updateData():
    try:
        guild = client.get_guild(GUILD_ID)
        bot_account = guild.get_member(BOT_ID)
        raceDetails = nextEvent(nextRace())
        nickname = raceDetails[1] + ': ' + raceDetails[2]
        watchingActivity = raceDetails[0]
        await bot_account.edit(nick=nickname)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=watchingActivity), status=discord.Status.online)
        logging.info(nickname)
        logging.info(watchingActivity)

    except RuntimeError:
        logging.error(
            'Failed to run updateData(): Runtime Error', exc_info=True)
    else:
        logging.info('Some other issue', exc_info=True)


@client.event
async def on_ready():
    logging.info('Logging in as {0.user}'.format(client))
    if not updateData.is_running():
        updateData.start()


client.run(TOKEN)
# nextEvent(nextRace())
