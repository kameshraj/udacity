#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

"""
Connect to the PostgreSQL database.
Returns a list of database connection and the cursor

Args: none

returns: none
"""
def connect():
    db = psycopg2.connect('dbname=tournament')
    cur = db.cursor()
    return db, cur

"""
commit the change and close the db connection

Args:
    db: connection handle to database

returns: none
"""
def commit_n_close(db):
    db.commit()
    db.close()

"""
Clean up records in matches table.
Removes all matches row from table

Args: none

returns: none
"""
def deleteMatches():
    db, cur = connect()
    cur.execute('DELETE FROM Matches')
    commit_n_close(db)

"""
Clean up records in player table.
Remove all players row from table

Args: none

returns: none
"""
def deletePlayers():
    db, cur = connect()
    cur.execute('DELETE FROM Players')
    commit_n_close(db)

"""
returns number of players in player table

Args: none

returns: none
"""
def countPlayers():
    db, cur = connect()
    cur.execute('SELECT count(*) FROM Players')
    cnt = cur.fetchall()[0][0]
    db.close()
    return cnt

"""
Adds a player to the tournament database.

The database assigns a unique serial id number for the player.  (This
should be handled by your SQL database schema, not in your Python code.)

Args:
  name: the player's full name (need not be unique).

returns: none
"""
def registerPlayer(name):
    db, cur = connect()
    sql = "INSERT INTO Players (name) VALUES (%s)"
    data = bleach.clean(name) # making it safe
    cur.execute(sql, [data])
    commit_n_close(db)

"""
Returns a list of the players and their win records, sorted by wins.

The first entry in the list should be the player in first place, or a player
tied for first place if there is currently a tie.

Args: none

Returns:
  A list of tuples, each of which contains (id, name, wins, matches):
    id: the player's unique id (assigned by the database)
    name: the player's full name (as registered)
    wins: the number of matches the player has won
    matches: the number of matches the player has played
"""
def playerStandings():
    db, cur = connect()
    cur.execute("SELECT id, name, wins, matches FROM Players ORDER BY wins")
    rows = cur.fetchall()
    db.close()
    return rows

"""
Records the outcome of a single match between two players.

Args:
  winner:  the id number of the player who won
  looser:  the id number of the player who lost

returns: none
"""
def reportMatch(winner, looser):
    db, cur = connect()

    # make the inputs safe
    winner = bleach.clean(winner)
    looser = bleach.clean(looser)

    # update wins for player
    sql = "UPDATE Players SET Wins = Wins + 1 WHERE id = %s;"
    cur.execute(sql, [winner])

    # update match played for players
    sql = "UPDATE Players SET matches = matches + 1 WHERE id in (%s, %s);"
    cur.execute(sql, [winner, looser])

    # Insert the players into table
    sql = "INSERT INTO Matches VALUES (%s, %s);"
    cur.execute(sql, [winner, looser])
    commit_n_close(db)

"""
Returns a list of pairs of players for the next round of a match.

Assuming that there are an even number of players registered, each player
appears exactly once in the pairings.  Each player is paired with another
player with an equal or nearly-equal win record, that is, a player adjacent
to him or her in the standings.

Args: none

Returns:
 A list of tuples, each of which contains (id1, name1, id2, name2)
   id1: the first player's unique id
   name1: the first player's name
   id2: the second player's unique id
   name2: the second player's name
"""
def swissPairings():
    db, cur = connect()
    cur.execute("""SELECT t.pid1, t.pname1, t.pid2, t.pname2 FROM (
                      SELECT id as pid1, name as pname1,
                      LEAD(id) OVER (ORDER BY wins DESC) as pid2,
                      LEAD(name) OVER (ORDER BY wins DESC) as pname2,
                      row_number() OVER (ORDER BY wins DESC) as row
                      FROM players
                  ) t WHERE t.row % 2 = 1""")
    rows = cur.fetchall()
    db.close()
    return rows
