Udacity Fullstack Web Developer
===============================

Tournament project
------------------
Python files for udacity **Full Stack Web Developer** Nano Degree course's Tournament project

- **tournament.sql** - File with SQL commands to create the database and tables for the project. You can copy the lines from this file and run it in PSQL shell or invoke everything in this file using command


    psql -f tournament.sql

- **tournament.py** - Actual module which provides all supporting functional calls for this project
- **tournament_test.py** - Unit test for this project

To unit test this project execute

    python tournament_test.py

----------

Project file break down
-----------------------
**tournament_test.py**: unit test case for the project
- **testDeleteMatches()**: Check if we can delete all matches record from the db
- **testDelete()**: Check if we can delete all matches & players record from the db
- **testCount()**: Check to see players count is 0 after deleting all matches & players
- **testRegister()**: Registers a players and checks countPlayers returns 1
- **testRegisterCountDelete()**: Registers 4 players and checks the countPlayers to match 4. Deletes all players and checks countPlayers to match 0
- **testStandingsBeforeMatches()**: Test players standing result. Will add 2 players and check playerStanding return 2. Checks wins and matches are 0 (before a tournament is started). Also checks if the name appears in order of insert
- **testReportMatches()**: Test match result and verifies winner has matches played and wins updated
- **testPairings()**: Test after 1 match players with 1 win will be paired

----------

**tournament.py** python script with all functions. This will import psycopg2 & bleach. Please install these modules using *pip* or *easy_install*

    pip install psycopg2
    pip install bleach

- **connect()**: Will open connect to the tournament database and  return a list of db handle and a cursor to execute SQL commands
- **commit_n_close(db)**: Helper method to commit the change and close the db connection
	- Args
		- db: Handle to database connection
- **deleteMatches()**: Will delete all match records in the match table
- **deletePlayers()**: Will delete all players record from players table
- **countPlayers()**: Return number of players in players table
- **registerPlayer(name)**: Insert a new player to players table
	- Args
		- name: name of the player to insert
- **playerStandings()**: Return a list of players ordered by number of wins
- **reportMatch(winner, looser)**: Records wins and matches played for players
	- Args
		- winner: Player who win the match. 
		- looser: player who lost the match
- **swissPairings()**: return a list of Players paired up for next match based on their winning records