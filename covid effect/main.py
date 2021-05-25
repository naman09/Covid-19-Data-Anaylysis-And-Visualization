import json
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import os
import time

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

data = []
with open("covid-db.txt","r") as f:
    data = json.load(f)

data = data['cases_time_series']

dates = [row['dateymd'] for row in data]

cases = [int(row['dailyconfirmed']) for row in data]
deaths = [100*int(row['dailydeceased']) for row in data]
recovered = [int(row['dailyrecovered']) for row in data]

date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]

plt.title("Covid Effect On India")
plt.scatter(date_objects, cases, label="daily cases")
plt.scatter(date_objects, deaths, label="deaths (times 100)")
plt.scatter(date_objects, recovered, label="recovered")
plt.legend()
plt.ylabel("Cases")
plt.xlabel("Time")
plt.show()
