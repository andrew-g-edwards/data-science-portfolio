# Armagetron Advanced SBMM Algorithm
I was tasked with creating a skill-based match making algorithm for multi-player online indie game, Armagetron Advanced. The main game-mode is a competitive 6v6 "Control" type called Fortress. Since the community for this game is smaller than commercially successful games, the skill-set represented in your average 12 person lobby can be very diverse. Random teammates was too imbalanced, and the game lacked infrastructure for a captain system. 

I built an algorithm that sorts the entire player base based on performance-driven skill indicators, and separates players into 7 categories of play-style. When 12 players join the Queue to play, my algorithm generates evenly matched teams with options to reroll the teams or substitute in a player. 

[Dashboard #1](https://public.tableau.com/app/profile/andrew.g.edwards/viz/FortStats/CTRATKS)
[Dashboard #2](https://public.tableau.com/app/profile/andrew.g.edwards/viz/FortTierControlPanel/Dashboard1)

## Technical Skills Utilized
- Python
- PANDAS
- Google Sheets
- Tableau
- Discord API

## Data Harvesting
My colleague wrote a script to track each players' grid position at a tick rate of .1 seconds. From this info we could create logic and math to deduce certain players' habits, gameplay, and consistency in rounds of Fortress. After logging hundreds of rounds of gameplay, I felt the dataset was gained enough volume to start to sort players with inegrity. Data was outputted into a spreadsheet [here](https://docs.google.com/spreadsheets/d/16bRczYQ67d-naU9cHHas0htSFBct_ruu4xmcdI88Q28/edit#gid=2025326523).

## Data Analysis
Fortress has 4 positional categories for each teams' players. Defence, Sweeper, Winger, Center. Some players excel at some positions and are weaker at others, where the best players are elite at all. Taking a player's skill in each, combined with their likelihood to play each, was the most important consideration. To better look at each player's prowess in certain areas that are likely to influence match, I built this [TABLEAU DASHBOARD](https://public.tableau.com/app/profile/andrew.g.edwards/viz/FortStats/CTRATKS).
