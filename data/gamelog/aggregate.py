import os
import re
import create_db as DbConn
from sqlite3 import Error
import sys

PLAYER_AVG = {}
YEAR_PLAYER = {}
QB_DATA = {}
DB_CONN = DbConn.create_connection()
QB_COL = {}
DEF_COL = {}

def getYearTeam(key):
    yearMatch = re.search('(\d{4})(.*)', key)
    if yearMatch:
        return (yearMatch.group(1), yearMatch.group(2))
    return None

def fields(cursor):
    """ Given a DB API 2.0 cursor object that has been executed, returns
    a dictionary that maps each field name to a column index; 0 and up. """
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1

    return results

def fetchPlayers(year, team):
    global DB_CONN
    sql = "SELECT name FROM defense WHERE year = " + str(year) + " AND team = \'" + team + "\'"
    cur = DB_CONN.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append(row[0])
    return result

def fetchQB():
    global DB_CONN
    global QB_DATA
    global QB_COL
    cur = DB_CONN.cursor()
    cur.execute("SELECT * FROM qbdata")
    rows = cur.fetchall()
    QB_COL = fields(cur)
    for row in rows:
        date = str(row[QB_COL["year"]]) + row[QB_COL["game_date"]]
        QB_DATA[date] = row
    #print QB_DATA

def getPlayerStats(result, player, year):
    global DB_CONN
    global DEF_COL
    cur = DB_CONN.cursor()
    sql = "SELECT game_played, total_tackles, sack, interceptions from defense where name = \"" + player + "\" AND year = " + year
    cur.execute(sql)
    rows = cur.fetchall()
    DEF_COL = fields(cur)
    for row in rows:
        game_played = row[DEF_COL["game_played"]]
        total_tackles = row[DEF_COL["total_tackles"]]
        sack = row[DEF_COL["sack"]]
        interceptions = row[DEF_COL["interceptions"]]
        avg_tackles = float(total_tackles)/float(game_played)
        avg_sacks = float(sack)/float(game_played)
        avg_interception = float(interceptions)/float(game_played)
        result["total_tackle"] += avg_tackles
        result["total_sack"] += avg_sacks
        result["total_interception"] += avg_interception
        result["players"] += 1 #only count players if they have record from year before

def main():
    #1. First get all games played, 128 of them
    fetchQB()
    #2. Iterate the map
    global QB_DATA
    global YEAR_PLAYER
    for date, qb in QB_DATA.items():
        year = qb[QB_COL["year"]]
        opp = qb[QB_COL["opponent"]].lower()
        #print (year, opp)
        YEAR_PLAYER[str(year) + opp] = fetchPlayers(year, opp)
        #3. For each year and team, get a list of all players of that team that year
    for key, value in YEAR_PLAYER.items():
        #4. Iterate player list, sum and avg the performance from the year before
        year, team = getYearTeam(key)
        target_year = int(year) - 1
        #print (year, target_year)
        team_stats = {
            "year" : year,
            "team" : team,
            "players" : 0,
            "total_tackle" : 0.0,
            "avg_tackle" : 0.0,
            "total_interception" : 0.0,
            "avg_interception" : 0.0,
            "total_sack" : 0.0,
            "avg_sack" : 0.0
        }
        for player in value:
            #5. query the player data from the previous year, average stats
            getPlayerStats(team_stats, player, str(target_year))
        team_stats["avg_tackle"] = team_stats["total_tackle"]/float(team_stats["players"])
        team_stats["avg_interception"] = team_stats["total_interception"]/float(team_stats["players"])
        team_stats["avg_sack"] = team_stats["total_sack"]/float(team_stats["players"])
        print team_stats
        #6. Once sum is complete, write a row to correlation

main()