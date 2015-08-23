#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# NOTE: this implementation relies on 2 tables: 
# 	matches ('winner', 'loser')
#	players (id, 'name')


import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

# Drop all rows from the matches table.

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect();
    c = conn.cursor();
    c.execute("delete from matches;")
    conn.commit()
    conn.close()

# Remove all rows from the players table.

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect();
    c = conn.cursor();
    c.execute("delete from players;")
    conn.commit()
    conn.close()

# Returns the count of the players table.

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect();
    c = conn.cursor();
    c.execute("select count(*) from players;")
    num = int(c.fetchall()[0][0])
    conn.commit()
    conn.close()
    return num

# Important: the name is inserted as value, not a quoted
# value, to prevent script injection.

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect();
    c = conn.cursor();
    c.execute("insert into players (name) values (%s);" , (name,))
    conn.commit()
    conn.close()

# The standings call is to a view defined out of matches and players.

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect();
    c = conn.cursor();
    c.execute("select * from standings;")
    return c.fetchall()
    conn.commit()
    conn.close()

# Each member of the tuple is inserted as a value, not as a 
# quoted value, to avoid script injection.

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect();
    c = conn.cursor();
    c.execute("insert into matches (winner, loser) values (%s, %s);" , 
				   (winner, loser))
    conn.commit()
    conn.close()

# This implementation does not yet qualify for extra credit.    	 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings =  playerStandings()
    
    # Initialize an empty array to return the tuples in.

    pairings = []

    # This is the simplest, instructed method.
    # So long as there's at least 2 left, loop through by 2.
    # This does not yet deal with odd numbers of contestants. 

    for x in range(0, len(standings)-1, 2):
	tuple = (standings[x][0],
                 standings[x][1],
                 standings[x+1][0],
                 standings[x+1][1])
        pairings.append(tuple)	
    return pairings;

# This simply checks whether id1 and id2 have ever played before
# by checking to see if there is a column where either id1 is 
# the winner and id2 is the loser, or vice versa.

def hasPlayedBefore(id1, id2):
    """Checks to see if name1 and name2
       have ever played against one another.
    """
    conn = connect();
    c = conn.cursor();
    c.execute("""
              select * from matches where 
              matches.winner = %s and matches.loser = %s
              or matches.winner = %s and matches.loser = %s""",
              (id1, id2, id2, id1))
    numMatches = len(c.fetchall())
    conn.commit()
    conn.close()
    if (numMatches == 0):
       return False
    else:
        return True

# An extension for extra credit. It can be tested by replacing test calls
# in tournament_test.py to swissPairings() to swissPairingsExperimental().

def swissPairingsExperimental():
    """This is identical to swissPairings() except it attempts some of the
    extra credit conditions.

    First, it examines if there is a unique player with the most wins.

    According to Udacity documentation, only when the competition is complete
    should there be a winner with a unique non-zero number of wins.

    If there, then the algorithm does not report back a pairing, since 
    the competition is over.
    """
    standings =  playerStandings()
    
    # Check for unique, non-zero winner.
    # We assume at least two players. If you've got 1 player, 
    # there's no point in having a tournament!

    if (len(standings) < 2):
	print('Not enough players for a tourney!')
	return

    mostWinnings = standings[0]
    secondMostWinnings = standings[1]
    
    # Check if the winningest player has both non-zero wins
    # and more winnings the second winningest player.

    # If both conditions are met, then the Swiss tourney
    # is over! The winner's name is printed.
   
    if (mostWinnings[2] > secondMostWinnings[2]):
	print('There is a unique winner: ' + str(standings[0][1]) + '!')
        return

    # Initialize an empty array to return the tuples in.

    pairings = []

    # Uniqueness of pairings:
    # Keep track of who has been assigned a match.

    matchPlaced = [False] * len(standings)
    index = 0;

    # All the pairings are done once each has been placed in
    # a match. We use the matchPlaced array to both check
    # when we're done and to increment the index.
    
    while(sum(matchPlaced) < len(standings)):	
        if(not matchPlaced[index]):
	   index2 = index + 1
           # Look for the first next index that neither
           # has been placed in a match nor played the
           # index in question.           
           
	   # Once you find the appropriate partner, add
           # the tuple.
	   while(hasPlayedBefore(standings[index][0], 
                                 standings[index2][0])
                 or
                 matchPlaced[index2]):
                 index2 += 1   
	   tuple = (standings[index][0],
                 standings[index][1],
                 standings[index2][0],
                 standings[index2][1])
           pairings.append(tuple)
           matchPlaced[index] = True
           matchPlaced[index2] = True	
        index+= 1
    return pairings
