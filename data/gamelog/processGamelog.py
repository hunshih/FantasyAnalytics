import os
import re
import create_db as DbConn
from sqlite3 import Error
import sys

def clean(str):
    cleanString = re.sub('\W+','', str)
    return cleanString

def combine(ary):
    output = ""
    size = len(ary)
    count = 1
    for item in ary:
        output += item;
        if count < size:
            output += ","
        count += 1
    output += "\n"
    return output

def cleanDate(date):
    dateMatch = re.search('(\w{2})/(\w{2})', date)
    if dateMatch:
        #print str(dateMatch.group(1)) + str(dateMatch.group(2))
        return str(dateMatch.group(1)) + str(dateMatch.group(2))
    return ""

def isHome(str):
    if "@" in str:
        return 1
    return 0

def getScore(score):
    scoreMatch = re.search('(\d*)-(\d*)', score)
    if scoreMatch:
        return (scoreMatch.group(1), scoreMatch.group(2))
    return None

def create_ms(conn, player):
    """
    Create a new project into the projects table
    :return: player id
    """
    try:
        sql = """ INSERT or REPLACE INTO qbdata(name, team, year, game_date, week, opponent, home, result, score,
                                    op_score, played, started, completion, pass_attempt, percentage, pass_yards,
                                    yard_per_attempt, td, interception, sacked, sacked_yards, qb_rating, rush_attempt,
                                    rushed_yards, avg_rushed_yards, rush_td, fum, fum_lost)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, player)
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print "Error {}:".format(e.args[0])
        sys.exit(1)

def process():
    conn = DbConn.create_connection()
    #print conn
    #target = open("perflog.csv", "w")
    dirFiles = os.listdir('.') #list of directory files
    dirFiles.sort() #good initial sort but doesnt sort numerically very well
    sorted(dirFiles) #sort numerically in ascending order
    for filename in dirFiles:
        if filename.endswith(".csv"): 
            #print(filename)
            yearMatch = re.search('.*_(\d{4}).csv', filename)
            if yearMatch:
                year = yearMatch.group(1)
                with open(filename, "r") as lines:
                    lineNum = 0
                    for line in lines:
                        if lineNum < 1:
                            lineNum += 1
                            continue
                        else:
                            name = "Matthew Stafford"
                            data = line.split(',')
                            week = data[0]
                            date = cleanDate(data[1])
                            opp = clean(data[2])
                            team = "det"
                            home = isHome(data[2])
                            result = data[3][0]
                            (score, opponent_score) = getScore(data[3])
                            played = data[4]
                            started = data[5]
                            comp = data[6]
                            pass_att = data[7]
                            pct = data[8]
                            pass_yds = data[9]
                            avg = data[10]
                            pass_td = data[11]
                            interception = data[12]
                            sck = data[13]
                            sck_yards = data[14]
                            qb_rate = data[15]
                            rush_att = data[16]
                            rush_yrds = data[17]
                            rush_avg = data[18]
                            rush_td = data[19]
                            fum = data[20]
                            fum_los = data[21].strip()
                            player = (name, team, year, date, week, opp, home, result, score,
                                opponent_score, played, started, comp, pass_att, pct, pass_yds,
                                avg, pass_td, interception, sck, sck_yards, qb_rate, rush_att,
                                rush_yrds, rush_avg, rush_td, fum, fum_los)
                            #print player
                            create_ms(conn, player)


def main():
    process()

if __name__ == '__main__':
    main()
