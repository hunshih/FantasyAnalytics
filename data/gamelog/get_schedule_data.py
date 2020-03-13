#!/usr/bin/python
import scrapelib as scraper
import re #need a separate regex lib
from time import strptime

URL_FORMAT = 'http://www.nfl.com/schedules/%d/REG/%s'
TEAM_CITY_MAP = {}
# All Regex's
DATE_REG = r"<span class=\"mon\">(\w{3})</span><span class=\"day\">(\d{2})"
TEAM_REG = r"team-logo away ([a-zA-Z]*)\".*data-score-mobile=\"(\d*)\".*team-logo home ([a-zA-Z]*)\".*data-score-mobile=\"(\d*)\""

def createUrl(year, team):
    return 'http://www.nfl.com/schedules/%d/REG/%s' % (year, team)

def teamCityMapping():
    file = open("team_name_city.txt", "r")
    global TEAM_CITY_MAP
    Lines = file.readlines()
    for line in Lines:
        line = (line.strip()).split(",")
        TEAM_CITY_MAP[line[0]] = line[1]

def createDate(dateArry, year):
    # This function assumes dateArry contains [ Month, Day ]
    # returns date formate YYYYMMDD
    return 10000 * year + 100 * strptime(dateArry[0],'%b').tm_mon + int(dateArry[1])

def extractSchedule(data, year):
    # Fields to extract: date, home, away, score, away_score, win
    global DATE_REG
    result = {}

    # declare all arrays
    dates = []
    home = []
    away = []
    score = []
    op_score = []
    win = []

    # get all dates
    gameDates = re.findall(DATE_REG, data)
    for gameDate in gameDates:
        dates.append( createDate(gameDate,year) )
    result['dates'] = dates

    # get all home team


    # get all away team


def main():
    teamCityMapping()
    global TEAM_CITY_MAP
    print TEAM_CITY_MAP
    # scrape single page
    

    result = scraper.scrape_single('http://www.nfl.com/schedules/2003/REG/49ERS')
    if result != None:
        #print(result)
        print createUrl(1970, '49ERS')
        extractSchedule(result, 1970)
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