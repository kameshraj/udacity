-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Connect to some default database to delete the database
\c tournament
DROP TABLE Players;
DROP TABLE matches;

\c vagrant
DROP DATABASE tournament;

CREATE DATABASE tournament;
\c tournament

CREATE TABLE Players (Id SERIAL PRIMARY KEY, Name VARCHAR(250) not NULL , Wins INTEGER DEFAULT 0, Matches INTEGER DEFAULT 0);
CREATE TABLE Matches (Id1 INTEGER not NULL, Id2 INTEGER);
