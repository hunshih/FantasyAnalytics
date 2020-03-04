#!/usr/bin/python
import scrapelib as scraper
import re #need a separate regex lib

URL_FORMAT = 'http://www.nfl.com/schedules/%d/REG/%s'
TEAM_CITY_MAP = {}
# All Regex's
DATE_REG = r"<span class=\"mon\">(\w{3})</span><span class=\"day\">(\d{2})"

def createUrl(year, team):
    return 'http://www.nfl.com/schedules/%d/REG/%s' % (year, team)

def teamCityMapping():
    file = open("team_name_city.txt", "r")
    global TEAM_CITY_MAP
    Lines = file.readlines()
    for line in Lines:
        line = (line.strip()).split(",")
        TEAM_CITY_MAP[line[0]] = line[1]

def extractSchedule(data):
    # Fields to extract: date, home, opponent, score, op_score, win
    global DATE_REG
    result = {}
    re.findall(DATE_REG, data)



def main():
    teamCityMapping()
    global TEAM_CITY_MAP
    print TEAM_CITY_MAP
    # scrape single page
    
    result = scraper.scrape_single('http://www.nfl.com/schedules/2003/REG/49ERS')
    if result != None:
        #print(result)
        print createUrl(1970, '49ERS')
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