#!/Users/rohan/miniconda/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import client

year = 2014
league_code = 'PL'

league = client.get_league(year,league_code)
teams = client.get_teams(league)

squad_values = []

import string_util

for t in teams["teams"]:
    squad_value = t["squadMarketValue"]
    if not squad_value:
        continue
    value = string_util.parse_currency(squad_value)
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
plt.title('Squad Values in the Premier League (%d)' % year)
plt.xticks(index + bar_width, tuple([x[0] for x in  squad_values ]),rotation='vertical')

plt.tight_layout()

plt.show()
