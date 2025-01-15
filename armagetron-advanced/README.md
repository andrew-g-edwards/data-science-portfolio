# Armagetron Advanced SBMM Algorithm
I was tasked with creating a skill-based match making algorithm for multi-player online indie game, Armagetron Advanced. The main game-mode is a competitive 6v6 "Control" type called Fortress. Since the community for this game is smaller than commercially successful games, the skill-set represented in your average 12 person lobby can be very diverse. Random teammates was too imbalanced, and the game lacked infrastructure for a captain system. 

I built an algorithm that sorts the entire player base based on performance-driven skill indicators, and separates players into 7 categories of play-style. When 12 players join the Queue to play, my algorithm generates evenly matched teams with options to reroll the teams or substitute in a player. 

[Dashboard #1](https://public.tableau.com/app/profile/andrew.g.edwards/viz/FortStats/CTRATKS)

[Dashboard #2](https://public.tableau.com/app/profile/andrew.g.edwards/viz/FortTierControlPanel/Dashboard1)

## Technical Skills Utilized
- Python
- PANDAS
- Google Sheets + gspread API
- Tableau
- Discord API

## Data Harvesting
My colleague wrote a script to track each players' grid position at a tick rate of .1 seconds. From this info we could create logic and math to deduce certain players' habits, gameplay, and consistency in rounds of Fortress. After logging hundreds of rounds of gameplay, I felt the dataset was gained enough volume to start to sort players with inegrity. Data was outputted into a spreadsheet [here](https://docs.google.com/spreadsheets/d/16bRczYQ67d-naU9cHHas0htSFBct_ruu4xmcdI88Q28/edit#gid=2025326523).

## Data Analysis
Fortress has 4 positional categories for each teams' players. Defence, Sweeper, Winger, Center. Some players excel at some positions and are weaker at others, where the best players are elite at all. Taking a player's skill in each, combined with their likelihood to play each, was the most important consideration. To better look at each player's prowess in certain areas that are likely to influence match, I built this [TABLEAU DASHBOARD](https://public.tableau.com/app/profile/andrew.g.edwards/viz/FortStats/CTRATKS).

This gave me an idea of how to algorthmically and dynamically sort players into a bucketed tier system. With a 6v6 environment and diverse skillset in the queue, the buckets must be granular enough to be accurate, but coarse enough so as to not consistently group the same players together on the same team. After simulating hundreds of lobbies with different amounts of buckets I decided that 7 was an appropriate compromise of randomness and accuracy. To visualize what these Tiers would look like against the player base I made this [CONTROL PANEL TABLEAU DASHBOARD](https://public.tableau.com/app/profile/andrew.g.edwards/viz/FortTierControlPanel/Dashboard1). This also tells me when and where certain players are over/under performing withing their tier and if I should have to adjust variables in my algorithm to make things more balanced.

## Implementation
Since Armagetron is an indie game from the 2000s with limited dev power, most of the gameplay is coordinated through a Discord server. To make it most accessible, I developed a [custom bot script](https://github.com/andrew-g-edwards/data-science-portfolio/blob/main/armagetron-advanced/tron-sbmm.py) using Discord's Python API. The script queues 12 players and then algorithmically sorts them into 2 balanced teams. All of the bucketed tier data is picked up from the stat-logging script endpoint in a google sheet. I call on the gspread API to populate the data structures within the SBMM script.
