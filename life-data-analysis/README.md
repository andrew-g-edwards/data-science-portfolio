# Life Data
Starting April 2022, I started tracking data about my everyday life, including mood, sleep, appetite, exercise, socializing, time spent outdoors, looking at a screen, working, alcohol and nicotine use, hygienic habits, the temperature, and the weather. I store all of this data in a Google Sheet with informative pivot tables, subsets, and formatting.

--> [2023 HEATMAP CALENDAR, TABLEAU DASHBOARD](https://public.tableau.com/app/profile/andrew.g.edwards/viz/lifedata2023/MOOD)<--

-> [TABLEAU DASHBOARD](https://public.tableau.com/app/profile/andrew.g.edwards/viz/Life-Data/UPKEEP?publish=yes) <-

The analysis aims to explore questions:
- Which attributes of a day seem correlate with mood?
- Which attributes imply causation to others?
- Which attributes have changed over time and in what way?
- How can I implement these discoveries to contribute to a more sustainable lifestyle?


## Technical Skills Utilized
- Python
- PANDAS
- Google Sheets
- Seaborn + Matplotlib
- Jupyter Notebooks
- Tableau

## Analysis

I tracked my lifestyle patterns for each day and asssigned a value for each field. Mood, food intake, exercise, socializing, nicotine, and alcohol, were all given a score from 1 to 10 based on my engagement for the day. Sleep, screen time, work, and outside time are all tracked by the hour. Whether I showered or not is a boolean. Weather score is that day's weather graded out of 4. 

**Correlation:**

To best see correlation between each field on a day to day basis, I produced a heat map.

<img width="1103" alt="Screen Shot 2022-11-30 at 12 07 09 PM" src="https://user-images.githubusercontent.com/116092004/204862330-994fdc45-bc18-4894-8590-6434ac0e7ba9.png">

To no surprise to me, being outside and socializing have the greatest correlation with my mood. Screen time also has a negative correlation with my mood, which is also unsurprising. Exercise and food intake are strongly correlated as well, making sense as my appetite is stimulated after good workout. Something that does surprise me is that nicotine and alcohol have a positive correlation with mood. I don't consider myself a big user of either of those, nor do I explicitly find joy in either of them.

In order to level out some potential outliers and explore this further, I grouped the data by week and created another heatmap comparing fields on a weekly basis.

<img width="1088" alt="Screen Shot 2022-11-30 at 12 43 44 PM" src="https://user-images.githubusercontent.com/116092004/204869966-575b8697-f08d-4bc0-8994-72f0b72a507d.png">

A lot of the same correlations still hold. Some key insights I can gain about my lifestyle are: I am more likely to work out when it is nice outside. When I exercise I get more sleep and eat more, could be because I tend to do all of these things more on weekdays. Screen time and outside time compete for the same hours everyday, giving a strong negative correlation. Nicotine and alcohol use play a big part in socializing, more so than mood directly. 

**Causation:**

I mentioned above that I was skeptical about nicotine and alcohol's relationship to my mood, but I would speculate from this heat map that socializing causes positive mood, and socializing causes more alcohol and nicotine opportunity. To dive into this further, I filtered out days where I used nicotine and didn't socialize vs. days I socialized and didn't use nicotine:

Days where socializing > 5 and nicotine < 5:

<img width="427" alt="Screen Shot 2022-11-30 at 11 55 14 AM" src="https://user-images.githubusercontent.com/116092004/204873627-c687e56c-51fa-4fc9-9e0d-8eead63295cd.png">

Days where nicotine > 5 and socializing < 5:

<img width="424" alt="Screen Shot 2022-11-30 at 1 10 23 PM" src="https://user-images.githubusercontent.com/116092004/204875369-aabf4436-ed81-4c06-a8e9-6a4ac33ff49c.png">

When I isolate both variables from the other, we can see that socializing has a much more measurable positive impact on my mood than nicotine does, averaging a mood almost 2.5 points higher. Nicotine usage without socializing, actually gives me an average mood that is lower than my total average mood for the entire dataset. This is parallel to my beliefs as I don't use a lot of nicotine nor do I particularly enjoy using it. I have deduced that socializing is causation for a good mood, and it also enables me to use nicotine, but is a strong enough variable that it can mitigate the negative effects nicotine has on my mood.

<img width="844" alt="Screen Shot 2022-11-14 at 11 11 17 AM" src="https://user-images.githubusercontent.com/116092004/204876727-bb2df511-b856-4df3-a616-fbf736c9a713.png">

To further investigate the relationship of nicotine & alcohol, as they relate to sleep and socializing I built this graphic in Tableau. Nicotine seems to be largely social, with some variance in correlation. Alcohol is a much more social variable, with dark green on the right and yellow nodes on the left. As these two variables increase in usage together, it is evident that it impacts my sleeping patterns for the worse.

<img width="843" alt="Screen Shot 2022-11-14 at 10 53 06 AM" src="https://user-images.githubusercontent.com/116092004/204877769-40c528e3-99aa-4b10-b254-398d9fd25acc.png">

Exploring more on what variables I believe to have direction causation with my mood, we can se here that there is a very direct relationship between socialization and mood. If my average mood for the week is >5, I was very social that week. Inversely, if my average mood was <4, I was anti-social that week, with no exceptions. For the most part, he big yellow nodes are high up on both axes, and the dark red nodes are lower down on both axes. Confirming what we already suspected: being outside and being social equates to me being happier, and staying anti-social and looking at a screen is a less happy experience.


**Change over Time:**

As I've collected more data everyday, I become more conscientious of my behavior and what seems to be making me more happy. I have made a conscious effort to spend more time outside as shown here:

<img width="917" alt="Screen Shot 2022-11-14 at 10 38 49 AM" src="https://user-images.githubusercontent.com/116092004/204878890-69adedc7-4e2c-447f-a8ed-ffb2eda6024e.png">

Spending more time outside over the months I've been tracking this has helped influence an upward trend in my mood. I have also tried to remain consistent with my socializing patterns.
As I continue to be mindful, I hope to continue engaging in activities and behavior that benefits me and my well-being and minimize those that have adverse effects.
