import scrapelib as scraper

def main():
    # scrape single page
    result = scraper.scrape_single('http://www.nfl.com/schedules/2003/REG/49ERS')
    if result != None:
        print(result)
    else:
        print('failed to scrape')
    ''' Pseuddo code '''
    # Get all years
    # Get all teams
    # Iterate over both
    # Scrape

main()