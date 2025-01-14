# Data Science Portfolio

This repository contains a catalog of Data Analytics/Science projects completed by me, for academic, professional, self-learning, and hobby purposes.

## Technical Skills Utilized
- Python
- PANDAS
- Google Sheets + gspread API
- Tableau
- Jupyter Notebook
- Google Cloud Platform (sheets API, cloud scheduler)
- JavaScript
- HTML / CSS
- Object-Oriented Programming
- Spotify API
- Discord API
- smtplib

## Contents
- [Armagetron Advanced](https://github.com/andrew-g-edwards/data-science-portfolio/tree/main/armagetron-advanced)
  - Developed a skill-based match making algorithm for a multi-player online game. Used gameplay data from the server logs to analyze the entire player base at large and draw distinction between skillset to create a hierarchy of rankings. My python script then uses those buckets of players to sort match making queues into balanced teams. 
- [Life Data Analysis](https://github.com/andrew-g-edwards/data-science-portfolio/tree/main/life-data-analysis)
  - I track data about my everyday life (sleep, mood, habits, weather, etc) since April 2022 and use it investigate causation and correlation between variables and to process into insightful visualizations using Python libraries and Tableau. I created a [heatmap calendar for the year 2023](https://public.tableau.com/app/profile/andrew.g.edwards/viz/lifedata2023/MOOD) as well as an initial [dashboard](https://public.tableau.com/app/profile/andrew.g.edwards/viz/Life-Data/UPKEEP?publish=yes) for an earlier dataset.
- [Spotify Wrapped Weekly](https://github.com/andrew-g-edwards/data-science-portfolio/tree/main/spotify-wrapped-weekly)
  - A script that calls the Spotipy API every few hours and logs my listening history into a Google Sheet using gspread API, PANDAS, and a scheduled GCP cron job. Another script to analyze the data, create charts, and send a weekly "wrapped" e-mail to myself using html, smtplib, and a local cron job.
