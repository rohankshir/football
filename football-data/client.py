from __future__ import unicode_literals
import requests
import json

base_url = "http://api.football-data.org/alpha/"

# get all the league codes for a soccer season
def get_league_codes(year):
    url = base_url + "soccerseasons"

    params = dict(
        season=year
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    return [x['league'] for x in data]

# Given a soccer season and a league code (e.g. PL for Premier League),
# get the league info
def get_league(year,code):
    url = base_url + "soccerseasons"

    params = dict(
        season=year
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    league = next(x for x in data if x['league'] == code)
    return league

# Get all teams info for given league object populated using
# get_league function
def get_teams(league):
    url = league['_links']['teams']['href']
    print url
    teams = requests.get(url=url)
    return json.loads(teams.text)




