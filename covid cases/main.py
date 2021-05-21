# Idea
'''
Get data from api https://api.covid19india.org/data.json
Then statewise draw bar graph
    For each bar show confirmed, recovered, death cases
'''

import matplotlib.pyplot as plt
import json
import os
import time
import requests

# run if date of txt file is old
def updateDataset():
    print("*****UPDATING DATASET******")
    URL = "https://api.covid19india.org/data.json"
    res = requests.get(URL)
    if res.status_code != 200:
        raise ApiError(f"GET/data/ {res.status_code}")
    data= res.json()
    with open('covid-db.txt','w') as f:
        json.dump(data, f, indent=4)


lastModified = os.path.getmtime('covid-db.txt')
if lastModified + 86400 < time.time():
    updateDataset()

def cmpFunc(e):
    if int(e['confirmed']) == 0:
        return 0
    return int(e['deaths'])/int(e['confirmed'])

data = []

with open('covid-db.txt','r') as f:
    data = json.load(f)

data = data['statewise'][1:]
data.sort(key=cmpFunc) # sort based on deaths/confirmed ratio
data = data[-20:] # Last 20 states

states = []
cases = {'confirmed':[],
         'deaths':[],
         'recovered':[]
         }
for entry in data:
    stateName = entry['state'][:15]
    states.append(stateName)
    cases['confirmed'].append(int(entry['confirmed']))
    cases['deaths'].append(int(entry['deaths']))
    cases['recovered'].append(int(entry['recovered']))

plt.title("State-wise covid cases in India")
plt.ylabel("States")
plt.xlabel("cases in millions")
plt.barh(states,cases['confirmed'])
plt.barh(states,cases['recovered'])
plt.barh(states,cases['deaths'])

plt.legend(["confirmed","recovered","deaths"])


plt.show()

