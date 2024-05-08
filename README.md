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
![Rummy result game.](https://github.com/winni50927/2024Spr_projects/blob/main/Rummy_result_example.png)


### Conclusion:

1. Does the player who goes first have a higher winning percentage?

Contrary to what might be expected, the answer is no. Players who act later have a higher chance of winning. This is because, in Rummikub, players can utilize tiles from the public pool (the river), which are laid down by others. The more tiles available in the river, the greater the chances that a player can meld their hand tiles effectively.

2. Does the first player to pass the cold_start threshold have a higher probability of winning?

Yes, players who are the first to meet the cold_start requirement (by playing one or multiple sets totaling at least 30 points) show a higher winning percentage. Specifically, they have over a 30% chance of winning, which is significantly higher than the winning rate of players who are not the first to pass this threshold.


### Future Work:

1. Players employ selective strategies have a higher probability of winning.
2. Players with the competence to reorganize more existing sets into new sets and runs are more likely to win.

### Usage:
Open the MC_Rummikub_core.py to start enjoying the Rummikub simulation!
If you want to see the detail of each game, please set up 1 for the number_games and modify the verbose in the monte_carlo_simulation to True. 

### Reference:
1. https://canvas.illinois.edu/courses/42165/pages/in-class-a-simplistic-simulation-of-viral-spre-dot-dot-dot?module_item_id=3108657
2. https://bd-boardgame.com/2015/10/23/邏輯桌遊-拉密-rummikub-數字麻將-以色列麻將-規則介紹/
3. https://mediaspace.illinois.edu/media/t/1_lawwsyso 老師做project的影片
4. 卡譚島：https://github.com/S1monXuan/2023Spr_projects_catan_simulation/blob/main/Monte_Carlo_Simulation_597.pptx
5. The idea of utilizing 1-52 to represent 1-13 in four suits comes from: Pei-Yi Ding http://squall.cs.ntou.edu.tw/cprog/practices/p05-3%20Poker%20hand%20ranking.pdf
6. The Object-Oriented-Design, stats, and Monte Carlo Simulation function of the Game are learned from: Mr. Weible, MC_rock_paper_scissors.py


