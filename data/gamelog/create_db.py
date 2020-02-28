#guide: http://www.sqlitetutorial.net/sqlite-python/creating-database/
import sqlite3
from sqlite3 import Error
 
def connection_impl(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None
 
def create_connection():
    """ legacy """
    connection_impl("/Users/henry/Desktop/FantasyAnalytics/data/player.db"):

def create_connection(db_file):
    """ proper api """
    connection_impl(db_file)

def create_player(conn, player):
    """
    Create a new project into the projects table
    :return: player id
    """
    sql = ''' INSERT or REPLACE INTO defense(name,year,team,position,game_played,solo_tackles,
    assist_tackles,total_tackles,sack,sack_yards,tfl,passes_defended,interceptions,interception_yards,
    long_interception,interception_td,fumble_forced,fumble_rec,fumble_td,kicks_blocked)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, player)
    return cur.lastrowid

def upsert(conn, data, year, team):
    with conn:
        player = (data.group(1), year, team, data.group(2), data.group(4), data.group(5), data.group(6),
            data.group(7),data.group(8),data.group(9), data.group(10), data.group(11), data.group(12),
            data.group(13), data.group(14), data.group(15), data.group(16), data.group(17), data.group(18),
            data.group(19))
        player_id = create_player(conn, player)

if __name__ == '__main__':
    main()




