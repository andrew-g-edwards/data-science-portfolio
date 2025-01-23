# Spotify Wrapped Weekly
As an avid music listener, why wait 12 months for Spotify Wrapped every year? Especially when all of your data is right there? This application tracks all of my listening data and provides me with my own "spotify wrapped" every single week.

## Technical Skills Utilized
- Python
- PANDAS
- Google Sheets + gspread API
- Google Cloud Platform (sheets API, cloud scheduler)
- JavaScript
- HTML / CSS
- Object-Oriented Programming
- smtplib
- API Orchestration (last.fm + Spotify APIs)

## Data Migration
I wrote a script that creates an instance of the Spotify API and passes my credentials into a class that in turn, logs all of my Spotify listening data into a PANDAS dataframe. This data includes when I listened to a track, the artist of the track, track name, album name, release date, popularity, song duration, etc. The data is processed and then sent through the gspread API into a google sheet. Since the API only calls your 50 most recent tracks, I elected to have this code run every three hours, so as to not lose and data, but also minimize API traffic as much as I can. I set up a cron job using the Google Cloud Scheduler to migrate this data every 3 hours.

## Data Analysis
I have another script that pulls the data from the Google Sheet where it's hosted and has a class to break it down into usable structures. I seperate the data by week, using the current week for analysis, and the previous week for comparison. Unique tracks and artists are counted, total listening time is tallied, and hourly listening patterns are processes. I provide tables for the Top Arists and Top Tracks, datapoints that compare last week's stats to the current week's, and create a heat map for daily and hourly listening data.

![heatmap](https://github.com/user-attachments/assets/03229ad9-1563-459a-b433-e10e57784882)

This analysis is then all packaged into an e-mail by way of HTML. I used CSS that emulates the themes and stylings of Spotify's branding.

<img src="https://github.com/user-attachments/assets/6aa9e434-6b22-4e1d-b963-91608becfd25" width="200">

This being a snippet of the weekly email on mobile. The email is then executed using the smtplib library with a weekly local cron job scheduler using my Mac's native LaunchAgent.

## API Orchestration
In October of 2024, Spotify chose to limit the data one can pull from their API. They took away song features, genre data, and the ability to pull album artwork. In order to achieve the same level of insight as the former spotify API, I created an instance of the last.fm API, which has user populated fields for genre, song tags, and album art. I joined the last.fm data with each track from my Spotify dataframe and store it in a new Google Sheet. I used this data to populate my email with new charts:

<img width="583" alt="genres" src="https://github.com/user-attachments/assets/4a67e9c6-afc9-42ae-b40e-b87f49b2aae7" />

<img width="584" alt="albums" src="https://github.com/user-attachments/assets/4635b3b9-7b53-45db-a7b6-3c2579797849" />

