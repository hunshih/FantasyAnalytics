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
    return rows

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
        print key, " ", len(value)
    #4. Iterate list, track sum
    #5. query the player data from the previous year, average stats
    #6. Once sum is complete, write a row to correlation

main()