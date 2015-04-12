#!/Users/rohan/miniconda/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json

base_url = "http://api.football-data.org/alpha/"

url = base_url + "soccerseasons"

params = dict(
    season=2014
 )
resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

league = next(x for x in data if x['league'] == "PL")
print "%s Code: %s " % ( league['caption'], league['league'] )
teams = requests.get(url=league['_links']['teams']['href'])
teams = json.loads(teams.text)

squad_values = []

import string_util
for t in teams["teams"]:
    print "%s Squad Value %s" % (t["name"], t["squadMarketValue"])
    value = string_util.parse_currency(t["squadMarketValue"])
    squad_values.append((t["name"],value))

#sort data
squad_values.sort(key=lambda x: x[1])

from matplotlib import pyplot as plt
import numpy as np


fig = plt.figure()

index = np.arange(len(squad_values))
bar_width = 0.35

ax = plt.subplot()
ax.bar(np.arange(len(squad_values)), [x[1] for x in  squad_values ],bar_width)

plt.xlabel('Teams')

plt.ylabel('Squad Values (€)')
plt.title('Squad Values in the Premier League')
plt.xticks(index + bar_width, tuple([x[0] for x in  squad_values ]),rotation='vertical')

plt.tight_layout()

plt.show()

