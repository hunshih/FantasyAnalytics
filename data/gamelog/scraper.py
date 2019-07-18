from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import os
import re
import create_db as DbConn
import time

DEFENSE_FILTER_FIRST = r"athlete\":{\"(.*?)\"dir\":\"desc\"}]}]}}"
DEFENSE_FILTER_SECOND = r"athlete\":{\"(.*?)\"dir\":\"desc\"}]}}"
DEFENSE_REGEX = r"name\":\"([a-zA-Z\.\-\'\ ]*)\".*?position\":\"(\w*).*?statGroups\":{\"title\":\"(\w*).*?gamesPlayed\",\"displayValue\":\"(\d*).*?soloTackles\",\"displayValue\":\"(\d*).*?assistTackles\",\"displayValue\":\"(\d*).*?totalTackles\",\"displayValue\":\"(\d*).*?sacks\",\"displayValue\":\"(\d*).*?sackYards\",\"displayValue\":\"(\d*).*?tacklesForLoss\",\"displayValue\":\"(\d*).*?passesDefended\",\"displayValue\":\"(\d*).*?interceptions\",\"displayValue\":\"(\d*).*?interceptionYards\",\"displayValue\":\"(\d*).*?longInterception\",\"displayValue\":\"(\d*).*?interceptionTouchdowns\",\"displayValue\":\"(\d*).*?fumblesForced\",\"displayValue\":\"(\d*).*?fumblesRecovered\",\"displayValue\":\"(\d*).*?fumblesTouchdowns\",\"displayValue\":\"(\d*).*?kicksBlocked\",\"displayValue\":\"(\d*)"
YEAR_REGEX = r"/season/(\d*)"
TEAM_REGEX = r"/name/([a-z]*)/season/"
FAIL = []
URLS = []
YEARS = {2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018}
REMAIN = [
    "https://www.espn.com/nfl/team/stats/_/name/mia/season/2011",
    "https://www.espn.com/nfl/team/stats/_/name/no/season/2015",
    "https://www.espn.com/nfl/team/stats/_/name/nyj/season/2012",
    "https://www.espn.com/nfl/team/stats/_/name/sea/season/2013"
]
DB_CONN = DbConn.create_connection();

def getInfo(url):
    global YEAR_REGEX
    global TEAM_REGEX
    year = 0
    team = ""
    yearMatch = re.search(YEAR_REGEX, url)
    teamMatch = re.search(TEAM_REGEX, url)
    if yearMatch:
        year = yearMatch.group(1)
    if teamMatch:
        team = teamMatch.group(1)
    return (year, team)

def fillGlobal():
    global URLS
    global YEARS
    with open("teamAbbrv.txt", 'r') as teams:
        for team in teams:
            team = team.strip();
            for year in YEARS:
                url = "https://www.espn.com/nfl/team/stats/_/name/" + team + "/season/" + str(year);
                URLS.append(url)

def processData(data, year, team):
    global DEFENSE_REGEX
    global DB_CONN
    dict = {}
    #1st pass. May miss the first defense player
    player_datum = re.findall(DEFENSE_FILTER_FIRST, data)
    for player_data in player_datum:
        player = re.search(DEFENSE_REGEX,player_data)
        if player and player.group(3) == "Defense":
            dict[player.group(1)] = player
    player_datum = re.findall(DEFENSE_FILTER_SECOND, data)
    for player_data in player_datum:
        player = re.search(DEFENSE_REGEX,player_data)
        if player and player.group(3) == "Defense":
            dict[player.group(1)] = player

    #get DB connection
    for name, stats in dict.items():
        DbConn.upsert(DB_CONN, stats, year, team)
        #print (name," : ", stats.groups()) 

def scrape_single(url):
    global FAIL
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                data = resp.content
                (year, team) = getInfo(url)
                processData(data, year, team)                   
            else:
                FAIL.append(url)

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        FAIL.append(url)



def scrape():
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    global FAIL
    global URLS
    count = 0
    threshold = len(URLS)/10
    for url in URLS:
        scrape_single(url)
        count += 1
        if count > threshold:
            print "completed " + str(count*10/(len(URLS)/10)) + " percent"
            threshold += len(URLS)/10
        time.sleep( 5 )

    if len(FAIL) == 0:
        print "All Success!"
    else:
        print FAIL
        print len(FAIL)

def scrapeSpecific():
    global REMAIN
    for url in REMAIN:
        scrape_single(url)
    if len(FAIL) == 0:
        print "All Success!"
    else:
        print FAIL
        print len(FAIL)

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def loadRegex():
    target = open("regex.csv", "r")
    global DEFENSE_REGEX
    DEFENSE_REGEX = target.read()

def main():
    fillGlobal()
    #scrape() #This scrapes all teams data
    scrapeSpecific() #This scrapes the ones that failed


main()