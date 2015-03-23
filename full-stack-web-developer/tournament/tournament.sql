-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Lets start fresh, drop the datbase if it exists
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (id SERIAL PRIMARY KEY, name VARCHAR(250) not NULL , wins INTEGER DEFAULT 0, matches INTEGER DEFAULT 0);
CREATE TABLE matches (player1 INTEGER not NULL REFERENCES players(id), player2 INTEGER REFERENCES players(id));
