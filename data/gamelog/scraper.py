from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import os
import re

DEFENSE_FILTER = r"athlete\":{\"(.*?)\"desc\"}]}]}}"
DEFENSE_REGEX = r"name\":\"([a-zA-Z\.\-\'\ ]*)\".*?position\":\"(\w*).*?statGroups\":{\"title\":\"(\w*).*?gamesPlayed\",\"displayValue\":\"(\d*).*?soloTackles\",\"displayValue\":\"(\d*).*?assistTackles\",\"displayValue\":\"(\d*).*?totalTackles\",\"displayValue\":\"(\d*).*?sacks\",\"displayValue\":\"(\d*).*?sackYards\",\"displayValue\":\"(\d*).*?tacklesForLoss\",\"displayValue\":\"(\d*).*?passesDefended\",\"displayValue\":\"(\d*).*?interceptions\",\"displayValue\":\"(\d*).*?interceptionYards\",\"displayValue\":\"(\d*).*?longInterception\",\"displayValue\":\"(\d*).*?interceptionTouchdowns\",\"displayValue\":\"(\d*).*?fumblesForced\",\"displayValue\":\"(\d*).*?fumblesRecovered\",\"displayValue\":\"(\d*).*?fumblesTouchdowns\",\"displayValue\":\"(\d*).*?kicksBlocked\",\"displayValue\":\"(\d*)"
def processData(data):
    global DEFENSE_REGEX
    #print DEFENSE_REGEX
    #DEFENSE_REGEX = r"" + re.escape(DEFENSE_REGEX)
    #players = re.findall(r"\{\"athlete\":{\"name\":\"(?P<name>[a-zA-Z\.\-\'\ ]*)\".*?position\":\"(?P<pos>\w*)",data)
    player_datum = re.findall(DEFENSE_FILTER, data)
    for player_data in player_datum:
        player = re.search("Keith Brooking",player_data)
        if player:
            print player_data
            print "============"
        #print player_data
        #print "=================="

    #player = re.search(DEFENSE_REGEX,player_data[0])
    #print defense_data.group(0)
        #player = re.search(DEFENSE_REGEX,player_data)
        #if player:
            #print player
    #for player in players:
    #    print player
    print len(player_datum)

def scrape(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                data = resp.content
                #target = open("dallas_2010.txt", "w")
                #target.write(resp.content)
                processData(data)
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

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
    #loadRegex()
    #print DEFENSE_REGEX
    url = 'https://www.espn.com/nfl/team/stats/_/name/dal/season/2010'
    scrape(url)


main()