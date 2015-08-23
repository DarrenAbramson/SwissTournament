-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create tournament database and connect to it. Included in instructions.

-- Assumes tournament db does not yet exist. Throws error otherwise.

CREATE DATABASE tournament;

-- Connect to database.

\c tournament;

-- Players are uniquely identified by numeric id, not name.

create table players(id serial primary key,
		     name text);

-- A combination of winner and loser should, in a swiss tournament,
-- involve unique pairs. This motivates the choice of primary key.

-- Matches must be played by players justifying the choices
-- of player id as foreign keys.

create table matches(winner integer references players(id), 
		     loser integer references players(id), 
		     primary key (winner, loser));

-- View used in creating standings. Returns ids and total
-- matches played (including 0) for each player.id.

create view playerMatches as
		select players.id, count(matches.*) as num
			from players left join matches
			on matches.winner = players.id OR 
			matches.loser = players.id
		group by players.id;

-- View used in creating standings. Returns ids and total
-- wins (including 0) for each player.id.


create view playerWins as
		select players.id, count(matches.*) as num
			from players left join  matches
			on matches.winner=players.id
		group by players.id;

-- View for standings. Left join of both players to each
-- of the above views to get wins and matches for each.		

create view standings as 
 	    select players.id, players.name, 
	 	   playerWins.num as wins, playerMatches.num as matches
		from players, playerMatches, playerWins
		where players.id = playerMatches.id and
		      players.id = playerWins.id
		order by wins desc;
