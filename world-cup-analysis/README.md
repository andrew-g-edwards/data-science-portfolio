# World Cup Data
Joined two datasets ([1](https://www.kaggle.com/datasets/evangower/fifa-world-cup?select=worldcups.csv), [2](https://www.kaggle.com/datasets/bartoszwajman/wc-overall)) to explore the history of the World Cup tournament and create meaningful visualizations.

Analysis aims to investigate:
 - How has the tournament grown over time in terms of team and fan attendance?
 - How have scoring patterns evolved over time? Are there measurable statistics that reflect changes in the way the game has been played?
 - Which nations have won the most over time?
 - Which nations have placed most consistently over time?

## Technical Skills Utilized
- Python
- PANDAS
- Plotly
- Jupyter Notebooks

## Analysis
**Tournament growth:**

<img width="800" alt="attendance" src="https://user-images.githubusercontent.com/116092004/204618126-56a4a9ec-5933-422d-b97f-150189aeb80c.png">

Surprising to find out the most highly attendend world cup was not only 28 years ago, but also in the USA where there was not yet a large culture around the sport. I believe this to be in part of the existing infrastructure (we have pre-existing large stadiums across the country), accessibility (the USA has dozens of international airports accross the country with reasonable airfare), and high proximal population. Attendance comes down to carry-capacity, accessiblity, and promotion, which the USA seemed to perfect.

<img width="850" alt="numteams" src="https://user-images.githubusercontent.com/116092004/204619595-2ca0b215-3e5d-4867-8a37-5fe7e8771fbf.png">

It makes sense that the tournament has expanded over time as more countries develop competitive teams, it becomes increasingly televised, and demand/revenue/resources increase. It is in FIFA's best interest to progressively expand the tournament, infact we will see an increase to 48 teams for the 2026 World Cup.

**Scoring Patterns:**

<img width="750" alt="goals" src="https://user-images.githubusercontent.com/116092004/204620869-af4eb8f2-62a6-49da-b7f3-387690180835.png">

At first glance it looks like goal scoring has increased over time, but this is just total goals without taking account the number of games played. Since we know from the graph above that the tournament has grown in size over time, we must take this information in respect to games played as a more telling metric of goal scoring patterns.

<img width="750" alt="avggoals" src="https://user-images.githubusercontent.com/116092004/204621546-ef0c7bb4-8de9-4d89-b10e-6d4873f87348.png">

Now we see that goals per game was very high early on in the world cup history, but has since reached a more consistent level coming within 2.5±.5 goals per match. I suspect these changes in patterns of goal-scoring to be attributed to a) fitness of players being better equipped to play full games over time, especially defenders. b) nations' rosters becoming more complete from top to bottom, as overall competition in the sport increases skill descrepencies are minimized. and c) changes to the off-side rule over time would disallow goals that previously would have been counted in past world cups.

**History of Champions:**

<img width="811" alt="champions" src="https://user-images.githubusercontent.com/116092004/204651049-54c06c11-7f5a-494f-8ba8-9996586c85a2.png">

Very few countries have been crowned world cup champion, with Italy, Germany, and Brazil almost comprising winners of 2/3 of all cups. It would seem like there are some powerhouses here, but which ones are 'dynasties'? Let's take a closer look at when these cups were won...

<img width="1095" alt="Screen Shot 2022-11-29 at 1 30 10 PM" src="https://user-images.githubusercontent.com/116092004/204651531-fb32b050-43fc-475f-90a3-e4a568c930f5.png">

Brazil and Germany have consistently won world cups throughout the history of the tournament, whereas Italy won a couple early on and had a large gap before winning two more. Brazil and Germany are common favorites to win the whole thing and for good reason. But what happens when they don't come in first?

<img width="1104" alt="Screen Shot 2022-11-29 at 1 30 25 PM" src="https://user-images.githubusercontent.com/116092004/204652544-9ddf960a-7775-4e8e-9167-001e41a96fcd.png">

Germany has reached the final a total of 8 times and won half of them. (Note: some of these achievements were as West Germany before the reunification of Germany). Netherlands has reached the finals three times and lost all of them. Brazil is more of an all-or-nothing team, winning the cup or facing an earlier elimination. Let's add in 3rd places for a better look of consistency...

<img width="1005" alt="Screen Shot 2022-11-29 at 1 30 44 PM" src="https://user-images.githubusercontent.com/116092004/204653119-f2cf0f2c-50fc-495d-8864-75ed837d0381.png">

Brazil is the winningest team in world cup history. Germany is the best bet to go far in any given world cup, reaching the top 1, 2 and 3, four times each.
Italy is an honorable mention with a very successful world cup history as well. Uruguay won two world cups early on and has not seen top 3 action since.

<img width="365" alt="Screen Shot 2022-11-29 at 4 38 28 PM" src="https://user-images.githubusercontent.com/116092004/204654038-c647ece0-35a2-4c47-892e-47fdec6c3c51.png">

<img width="357" alt="Screen Shot 2022-11-29 at 4 38 36 PM" src="https://user-images.githubusercontent.com/116092004/204654053-6a6ad9c9-144a-4c33-93e0-ba78c1fe4e2f.png">

<img width="338" alt="Screen Shot 2022-11-29 at 4 38 52 PM" src="https://user-images.githubusercontent.com/116092004/204654084-bc193265-58c7-4513-945c-b5f13aa22190.png">
