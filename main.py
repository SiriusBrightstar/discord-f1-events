import json
from datetime import datetime
from datetime import timedelta

data = json.load(open('F1_Events_Hash.json', 'r'))

with open('F1_Events_Hash.json', 'r') as jsonFile:
  dataF1 = json.load(jsonFile)

print(f'JSON File: {dataF1}')

eventList = []

for i in range(len(dataF1)):
    FP1 = dataF1[str(i+1)]['Free Practice 1']
    FP1_DO = datetime.strptime(FP1, '%d %b %H:%M')
    FP1_DO = FP1_DO.replace(year=2022)
    FP1_DO = FP1_DO + timedelta(hours=5, minutes=30)
    eventList.append(FP1_DO)
    FP2 = dataF1[str(i+1)]['Free Practice 2']
    FP2_DO = datetime.strptime(FP2, '%d %b %H:%M')
    FP2_DO = FP2_DO.replace(year=2022)
    eventList.append(FP2_DO)
    if (dataF1[str(i+1)]['TBD'] == 'F'):
      FP3 = dataF1[str(i+1)]['Free Practice 3']
      FP3_DO = datetime.strptime(FP3, '%d %b %H:%M')
      FP3_DO = FP3_DO.replace(year=2022)
      eventList.append(FP3_DO)
    else:
      SPRINT = dataF1[str(i+1)]['Sprint']
      SPRINT_DO = datetime.strptime(SPRINT, '%d %b %H:%M')
      SPRINT_DO = SPRINT_DO.replace(year=2022)
      eventList.append(SPRINT_DO)
    QUALI = dataF1[str(i+1)]['Qualifying']
    QUALI_DO = datetime.strptime(QUALI, '%d %b %H:%M')
    QUALI_DO = QUALI_DO.replace(year=2022)
    eventList.append(QUALI_DO)
    RACE = dataF1[str(i+1)]['Race']
    RACE_DO = datetime.strptime(RACE, '%d %b %H:%M')
    RACE_DO = RACE_DO.replace(year=2022)
    eventList.append(RACE_DO)

# def nextEvent():


print('Event List')
print(eventList[(22*5)-1])
print(len(eventList))
