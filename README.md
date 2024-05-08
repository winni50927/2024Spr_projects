# 2024Spr_projects

### Project Name: 
#### Succeed in Rummikub: Apply Monte Carlo Simulation in Unveiling What Could Bring Advantages to A Rummy Player.
![Rummy the board game.](https://github.com/winni50927/2024Spr_projects/blob/main/2015-10-23-16-17-33.jpg)


### Abstract:

Rummikub is a classic board game whose invention can be traced back to the time after World War II. The game has 106 tiles, including 2 sets of 1 - 13 in four colors and 2 wildcards. Each player will be randomly assigned 14 tiles initially, and the rule of the game requires players to use their own tiles or combine their tiles with public melds to create melds formed as runs (e.g. 5, 6, 7) or groups (e.g. 7, 7, 7) with at least 3 components. All melds created will become public melds that can be used by all players. If players cannot create any melds in their rounds, they need to draw a new tile. The winner is the first one to get rid of all of his or her tiles. 

In the final project, I plan to develop a Type II project, utilizing Monte Carlo Simulation to test the hypotheses, to determine those strategies or competence that can actually attribute to a higher probability of winning Rummikub games.


### Assumption:
1. Four players in a game.
2. The players' order to playe are fixed for now. Winni -> Peter -> Rachel -> Carol 
3. Each player can play multiple times in one round.
4. Each player will play all the tiles and melds they can play in each round, without reservation.

### Hypothesis:

1. Among four players, the Player who play in the first order get higher winning percentage.

2. The Player who is the first to pass the cold_start limit (must play one or multiple sets with a total value of at least 30 points.) has a higher probability of winning.


### Stats Result Example:

-----------------------------------------------------------------

Tournament Player Statistics:

Name             Win%      Won       Lost
-------------- ------ ----------- ----------
Winni            21.91%       2191       7809
Peter            23.69%       2369       7631
Rachel           26.74%       2674       7326
Carol            30.11%       3011       6989

First Cold_Start Winning States

Name                             Win%      Won       Lost
------------------------------ ------ ----------- ----------
Winni                           26.83%       1021       2785
Peter                           30.14%        840       1947
Rachel                          34.34%        679       1298
Carol                           39.65%        567        863
------------------------------ ------ ----------- ----------

Aggregate first_cold_start     31.07%       3107       6893
Average not_first_cold_start   22.98%       2298       7702


### Conclusion:

1. Does the player who goes first have a higher winning percentage?

Contrary to what might be expected, the answer is no. Players who act later have a higher chance of winning. This is because, in Rummikub, players can utilize tiles from the public pool (the river), which are laid down by others. The more tiles available in the river, the greater the chances that a player can meld their hand tiles effectively.

2. Does the first player to pass the cold_start threshold have a higher probability of winning?

Yes, players who are the first to meet the cold_start requirement (by playing one or multiple sets totaling at least 30 points) show a higher winning percentage. Specifically, they have a 33.4% chance of winning, which is significantly higher than the 16.6% winning rate of players who are not the first to pass this threshold.


### Future Work:

1. Players employ selective strategies have a higher probability of winning.
   
3. Players with the competence to reorganize more existing sets into new sets and runs are more likely to win.


