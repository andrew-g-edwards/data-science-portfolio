# Spotify Extended Listening History
I've been a Spotify user since 2015 and I requested my entire listening history. In this project I do a deep dive into my listening patterns over the last 10 years and chart how my music preferences have evolved.

## Technical Skills Utilized
- Python
- SQL
- Pandas
- Plotly / Matplotlib / seaborn
- JSON parsing
- Data Visualization
- Jupyter Notebook

## Data Analysis
Spotify gave me my data in 17 different JSON files. I wrote a loop to iterate through each of these and store all of the data into a dataframe. I then query the dataframe for my top 10 artists by play count for each year. With this data I then used Plotly to create an interactive sankey diagram with nodes for each artist, and a flow to illustrate the evolution and progression of my listening relationship with that artist.

In addition, I created a Jupyter Notebook where I connect my pandas dataframe to sqlite3. This allowed me to query the data easily and create insightful and compelling visualizations [here](https://github.com/andrew-g-edwards/data-science-portfolio/blob/main/spotify-top10-history/listening_history.ipynb).

## Visualization
<img width="1104" alt="sankey diagram" src="https://github.com/user-attachments/assets/9330adb6-4a8e-4a68-941a-19999e12f346" />


