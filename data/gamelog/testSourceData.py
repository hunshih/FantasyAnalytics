from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import time
import os
import re

FAIL = []
URLS = []
YEARS = {2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018}

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
        try:
            with closing(get(url, stream=True)) as resp:
                if not is_good_response(resp):
                    FAIL.append(url)

        except RequestException as e:
            log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            FAIL.append(url)
        count += 1
        if count > threshold:
            print "completed " + str(count*10/threshold) + " percent"
            threshold += len(URLS)/10
        time.sleep( 5 )

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


def main():
    global URLS
    global YEARS
    with open("teamAbbrv.txt", 'r') as teams:
        for team in teams:
            team = team.strip();
            for year in YEARS:
                url = "https://www.espn.com/nfl/team/stats/_/name/" + team + "/season/" + str(year);
                URLS.append(url)
    #print URLS
    scrape()
main()