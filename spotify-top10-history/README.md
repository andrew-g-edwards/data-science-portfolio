# Spotify Extended Listening History
I've been a Spotify user since 2015 and I requested my entire listening history. In this project I do a deep dive into my listening patterns over the last 10 years and chart how my music preferences have evolved.

## Technical Skills Utilized
- Python
- SQL
- Pandas
- Plotly / Matplotlib / seaborn
- JSON parsing
- Data Visualization + Animation
- Jupyter Notebook

## Data Analysis
Spotify gave me my data in 17 different JSON files. I wrote a loop to iterate through each of these and store all of the data into a dataframe. I then query the dataframe for my top 10 artists by play count for each year. With this data I then used Plotly to create an interactive sankey diagram with nodes for each artist, and a flow to illustrate the evolution and progression of my listening relationship with that artist.

In addition, I created a Jupyter Notebook where I connect my pandas dataframe to sqlite3. This allowed me to query the data easily and create insightful and compelling visualizations [here](https://github.com/andrew-g-edwards/data-science-portfolio/blob/main/spotify-top10-history/listening_history.ipynb).

## Top Artist Sankey Diagram
<img width="1104" alt="sankey diagram" src="https://github.com/user-attachments/assets/9330adb6-4a8e-4a68-941a-19999e12f346" />

## Bar Chart Race
I used flourish.studio to create an animated bar chart race for my top artists and listening habits evolution over time. I queried my data base to find a rolling 30-day total of my top artists, compounded every week. You can view it by clicking on the image below. 

[![click here]([https://img.youtube.com/vi/hLEvAWv1Bjs/0.jpg](https://github.com/user-attachments/assets/7784e9b9-61ec-403f-97f5-ad1edca1153e))](https://www.youtube.com/watch?v=hLEvAWv1Bjs&ab_channel=AndrewEdwards)

Here is the query and data manipulation I used to build the dataset used in the animation:

<img width="598" alt="bar chart query" src="https://github.com/user-attachments/assets/f7ea4509-6460-438f-a5c5-e353eae83f91" />


## Visualizations and Queried Tables
<img width="921" alt="listening metrics by year" src="https://github.com/user-attachments/assets/28d9eb1f-d04a-4e87-9b46-36d94d59b75e" />


<img width="900" alt="top songs by year" src="https://github.com/user-attachments/assets/9fe400c0-b877-4a13-9460-00e54e3c79c1" />


<img width="1120" alt="heatmap day vs. hour" src="https://github.com/user-attachments/assets/ef1343ac-f877-4dc8-a268-a62829ea3ff7" />


<img width="1131" alt="heatmap year vs. month" src="https://github.com/user-attachments/assets/a2eee154-fdd3-4d02-86f2-be6eed038246" />


<img width="1125" alt="phases" src="https://github.com/user-attachments/assets/fae19a39-873e-48c0-93b1-38a99ff21c31" />


<img width="590" alt="artist consistency" src="https://github.com/user-attachments/assets/cf4b1054-22f1-4b1b-a6ad-600dc3a89d78" />

<img width="640" alt="top minutes per stream" src="https://github.com/user-attachments/assets/9c85817d-5f16-474e-ad15-fdc1c34bcd76" />

<img width="659" alt="top completion rates" src="https://github.com/user-attachments/assets/9932a760-f204-4da7-94a1-79b2b90ce2b4" />
