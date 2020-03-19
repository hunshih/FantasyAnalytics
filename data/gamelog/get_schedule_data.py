#!/usr/bin/python
import scrapelib as scraper
import re #need a separate regex lib
from time import strptime

URL_FORMAT = 'http://www.nfl.com/schedules/%d/REG/%s'
TEAM_CITY_MAP = {}
TEAM_MAP = {}
# All Regex's
DATE_REG = r"<span class=\"mon\">(\w{3})</span><span class=\"day\">(\d{2})"
TEAM_REG = r"team-logo away ([a-zA-Z]*)\".*data-score-mobile=\"(\d*)\".*\n.*\n.*\n.*team-logo home ([a-zA-Z]*)\".*data-score-mobile=\"(\d*)\""

def createUrl(year, team):
    return 'http://www.nfl.com/schedules/%d/REG/%s' % (year, team)

def teamCityMapping():
    file = open("team_name_city.txt", "r")
    global TEAM_CITY_MAP
    Lines = file.readlines()
    for line in Lines:
        line = (line.strip()).split(",")
        TEAM_CITY_MAP[line[0]] = line[1]

def teamMapping():
    file = open("team_list.txt", "r")
    global TEAM_MAP
    Lines = file.readlines()
    for line in Lines:
        line = (line.strip()).split(",")
        TEAM_MAP[line[0]] = line[1]

def createDate(dateArry, year):
    # This function assumes dateArry contains [ Month, Day ]
    # returns date formate YYYYMMDD
    return 10000 * year + 100 * strptime(dateArry[0],'%b').tm_mon + int(dateArry[1])

def extractSchedule(data, year, sch_team):
    # Fields to extract: date, home, away, score, away_score, win
    global DATE_REG
    result = {}

    global TEAM_MAP

    # declare all arrays
    dates = []
    home = []
    away = []
    home_score = []
    away_score = []
    win = []

    # get all dates
    gameDates = re.findall(DATE_REG, data)
    for gameDate in gameDates:
        dates.append( createDate(gameDate,year) )
    result['dates'] = dates

    # get all teams and scores
    teams = re.findall(TEAM_REG, data)
    for team in teams:
        away.append(team[0])
        away_score.append( int(team[1]) )
        home.append(team[2])
        home_score.append( int(team[3]) )
        
        # decided if the team wins
        # Away wins. -1 gets last item
        if away_score[-1] > home_score[-1] :
            if sch_team == TEAM_MAP[away[-1]]:
                win.append(1)
            else:
                win.append(0)
        else:
            if sch_team == TEAM_MAP[away[-1]]:
                win.append(0)
            else:
                win.append(1)

    result['away'] = away
    result['away_score'] = away_score
    result['home'] = home
    result['home_score'] = home_score
    result['win'] = win

    print result
    return result


def main():

    #construct a global team map
    teamMapping()

    # scrape single page
    result = scraper.scrape_single('http://www.nfl.com/schedules/2003/REG/49ERS')
    if result != None:
        #print(result)
        print createUrl(1970, '49ERS')
        extractSchedule(result, 1970, '49ers')
    else:
        print('failed to scrape')
    
    ''' Pseuddo code '''
    # Get all years
    # Get all teams
    # Iterate over both
    # Scrape

if __name__ == "__main__":
    # execute only if run as a script
    main()