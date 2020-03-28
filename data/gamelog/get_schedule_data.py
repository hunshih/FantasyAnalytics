#!/usr/bin/python
import scrapelib as scraper
import re #need a separate regex lib
from time import strptime
import create_db as DbConn

URL_FORMAT = 'http://www.nfl.com/schedules/%d/REG/%s'
TEAM_CITY_MAP = {}
TEAMS = []
THRESHOLD = 5
# All Regex's
DATE_REG = r"<span class=\"mon\">(\w{3})</span><span class=\"day\">(\d{2})"
TEAM_REG = r"team-logo away ([a-zA-Z]*)\".*data-score-mobile=\"(\d*)\".*\n.*\n.*\n.*team-logo home ([a-zA-Z]*)\".*data-score-mobile=\"(\d*)\""

def percentage(year):
    return ((year - 1970)/50.0) * 100

def printPercentage(year):
    percent = percentage(year)
    global THRESHOLD
    if percent > THRESHOLD:
        print "Finished %d percent" % (percent)
        THRESHOLD = THRESHOLD + 5


#return True if data is from a valid page
def validData(data):
    return bool( re.findall(r"Regular Season Schedule", data) )

def createUrl(year, team):
    return 'http://www.nfl.com/schedules/%d/REG/%s' % (year, team)

def teamCityMapping():
    file = open("team_name_city.txt", "r")
    global TEAM_CITY_MAP
    Lines = file.readlines()
    for line in Lines:
        line = (line.strip()).split(",")
        TEAM_CITY_MAP[line[0]] = line[1]

def getTeamList():
    file = open("team_list.txt", "r")
    global TEAMS
    Lines = file.readlines()
    for line in Lines:
        TEAMS.append(line.strip())

def createDate(dateArry, year):
    # This function assumes dateArry contains [ Month, Day ]
    # returns date formate YYYYMMDD
    return 10000 * year + 100 * strptime(dateArry[0],'%b').tm_mon + int(dateArry[1])

def extractSchedule(data, year, sch_team):
    # Fields to extract: date, home, away, score, away_score, win
    global DATE_REG
    result = {}

    # declare all arrays
    dates = []
    home = []
    away = []
    home_score = []
    away_score = []
    win = []

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
            if sch_team == away[-1]:
                win.append(1)
            else:
                win.append(0)
        else:
            if sch_team == away[-1]:
                win.append(0)
            else:
                win.append(1)

    # get all dates
    gameDates = re.findall(DATE_REG, data)
    for gameDate in gameDates:
        dates.append( createDate(gameDate,year) )

    # put all result array into map
    result['dates'] = dates
    result['away'] = away
    result['away_score'] = away_score
    result['home'] = home
    result['home_score'] = home_score
    result['win'] = win

    # For debug, print result
    #print result
    return result


def main():

    # get the global team list
    global TEAMS
    getTeamList()

    # get database accessor
    db_conn = DbConn.connect_schedule_db()

    # write error to output file
    error = open("error.txt", "a")
    result_file = open("result.txt", "a")

    # Iterate from 1970 to 2019
    for year in range(1970, 2020):

        #show progress
        printPercentage(year)

        for team in TEAMS:
            # scrape single page
            data = scraper.scrape_single( createUrl(year, team) )
            if validData(data) == True:
                #print(data)
                result = extractSchedule(data, year, team)
                result_file.write( str(result) + "\n" )

                # Iterate over all games in the season
                for x in range(0,len(result["dates"])):
                    cur = db_conn.cursor()
                    sql = ''' INSERT or REPLACE INTO schedule(season,team,date,home,away,score,away_score,
                        win) VALUES(?,?,?,?,?,?,?,?) '''
                    schedule = (year, team, result["dates"][x], result["home"][x], result["away"][x], result["home_score"][x], 
                                result["away_score"][x], result["win"][x])
                    cur.execute(sql, schedule)
                    db_conn.commit()
            else:
                error.write( 'failed to scrape for ' + str(year) + " " + team + "\n")

    result_file.close()
    error.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()