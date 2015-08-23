# SwissTournament
### Full Stack Development P2: Tournament Results

This director provides the two files needed to pass all of the tests defined in `tournament_test.py`. 

I have implemented both a naive algorithm, `swissPairings()`, and another algorithm `swissPairingsExperimental()`. Both should pass all tests. The differences between the two are that the second adds:

* checking to see if the tournament has a minimum size (more than 1)
* checking to see if the tournament is over, i.e. has a unique winner
* guaranteeing that pairings are unique with respect to the tournament so far.

