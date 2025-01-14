import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from datetime import datetime
import pandas as pd
import numpy as np
import gspread
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
import os

class SpotifyLogger:
    def __init__(self, client_id, client_secret, redirect_uri, sheet_id, max_retries=3):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.max_retries = max_retries

        # Initialize Google Sheets client using application default credentials
        credentials = service_account.Credentials.from_service_account_info(
            # This assumes you've added your service account JSON content to env vars
            eval(os.environ.get('GOOGLE_SERVICE_ACCOUNT_INFO')),
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        gc = gspread.authorize(credentials)
        self.sheet = gc.open_by_key(sheet_id)
        self.worksheet = self.sheet.sheet1

        # Define Spotify scopes
        self.scope = " ".join([
            "user-read-recently-played",
            "user-top-read",
            "user-read-currently-playing",
            "user-read-private",
            "user-library-read"
        ])

        self.sp = self.initialize_spotify()

    def initialize_spotify(self):
        """Initialize Spotify client with refresh token"""
        try:
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
                open_browser=False,
                refresh_token=os.environ.get('SPOTIFY_REFRESH_TOKEN')
            )
            spotify = spotipy.Spotify(auth_manager=auth_manager)
            return spotify
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            return None

    def get_recent_tracks(self, limit=50):
        """Get recently played tracks and convert to DataFrame"""
        if not self.sp:
            print("Spotify client not properly initialized")
            return None

        try:
            recent_tracks = self.sp.current_user_recently_played(limit=limit)
            tracks_data = []

            total_tracks = len(recent_tracks['items'])
            print(f"\nFound {total_tracks} tracks to process")

            for idx, item in enumerate(recent_tracks['items'], 1):
                print(f"\nProcessing track {idx}/{total_tracks}...")

                track = item['track']
                played_at = item['played_at']

                # Basic track data
                track_data = {
                    'played_at': played_at,  # Rename 'timestamp' to 'played_at'
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'track_number': track['track_number'],
                    'artist_id': track['artists'][0]['id'],
                    'artist_name': track['artists'][0]['name'],
                    'album_id': track['album']['id'],
                    'album_name': track['album']['name'],
                    'album_release_date': track['album'].get('release_date'),
                    'album_release_date_precision': track['album'].get('release_date_precision', 'unknown'),
                    'album_type': track['album']['album_type'],
                    'duration_ms': track['duration_ms'],
                    'explicit': track['explicit'],
                    'popularity': track['popularity'],
                    'preview_url': track['preview_url'],
                    'external_urls_spotify': track['external_urls']['spotify']
                }

                # Get all artists if there are multiple
                all_artists = [artist['name'] for artist in track['artists']]
                track_data['all_artists'] = ', '.join(all_artists)

                tracks_data.append(track_data)
                print(f"Successfully processed: {track['name']}")
                time.sleep(0.1)

            # Convert to DataFrame
            df = pd.DataFrame(tracks_data)

            # Convert played_at to datetime
            df['played_at'] = pd.to_datetime(df['played_at'])

            # Handle different date formats and precisions
            def parse_release_date(row):
                date = row['album_release_date']
                precision = row['album_release_date_precision']

                if pd.isna(date):
                    return np.nan

                try:
                    if precision == 'year':
                        return pd.to_datetime(date, format='%Y')
                    elif precision == 'month':
                        return pd.to_datetime(date + '-01', format='%Y-%m-%d')
                    else:  # precision == 'day' or unknown
                        return pd.to_datetime(date)
                except:
                    return np.nan

            # Parse release dates
            df['album_release_date_parsed'] = df.apply(parse_release_date, axis=1)

            # Add derived time features
            df['play_year'] = df['played_at'].dt.year
            df['play_month'] = df['played_at'].dt.month
            df['play_day'] = df['played_at'].dt.day
            df['play_hour'] = df['played_at'].dt.hour
            df['play_day_of_week'] = df['played_at'].dt.day_name()

            # Add release year (safely) from 'album_release_date_parsed'
            df['release_year'] = df['album_release_date_parsed'].dt.year

            # Drop 'album_release_date_parsed' since it's already included in 'release_year'
            df.drop(columns=['album_release_date_parsed'], inplace=True)

            return df

        except spotipy.exceptions.SpotifyException as e:
            print(f"Error getting recent tracks: {str(e)}")
            return None

    def write_headers_if_needed(self):
        """Check if headers are present, if not, write them"""
        first_row = self.worksheet.row_values(1)
        if not first_row:
            headers = [
                'timestamp', 'track_id', 'track_name', 'track_number', 'artist_id',
                'artist_name', 'album_id', 'album_name', 'album_release_date',
                'album_release_date_precision', 'album_type', 'duration_ms', 'explicit',
                'popularity', 'preview_url', 'external_urls_spotify', 'all_artists', 'play_year',
                'play_month', 'play_day', 'play_hour', 'play_day_of_week', 'release_year'
            ]
            self.worksheet.insert_row(headers, 1)
            print("Headers written to sheet.")

    def push_to_google_sheets(self, df):
        """Push the DataFrame to Google Sheets"""
        if df is None or self.worksheet is None:
            print("No data to push to Google Sheets")
            return

        # Write headers only if they do not already exist
        self.write_headers_if_needed()

        # Get all existing data from the sheet
        existing_data = self.worksheet.get_all_values()
        print(f"\nFound {len(existing_data)} rows in sheet (including header)")

        # Skip header row and create a set of existing timestamps
        existing_timestamps = {row[0] for row in existing_data[1:]}
        print(f"\nExtracted {len(existing_timestamps)} existing timestamps")
        print("Sample of existing timestamps:", list(existing_timestamps)[:3])

        # Convert DataFrame timestamps to the same format as in sheets
        df_copy = df.copy()
        df_copy['played_at'] = df_copy['played_at'].dt.strftime('%Y-%m-%d %H:%M:%S.%f%z')

        print("\nSample of incoming timestamps:", df_copy['played_at'].head().tolist())

        # Print a few comparisons to debug
        for i, new_ts in enumerate(df_copy['played_at'].head()):
            print(f"\nChecking timestamp {i}: {new_ts}")
            print(f"Is in existing_timestamps?: {new_ts in existing_timestamps}")

        # Filter out rows that already exist
        new_rows = df_copy[~df_copy['played_at'].isin(existing_timestamps)]

        print(f"\nFound {len(new_rows)} new tracks to add")

        if len(new_rows) == 0:
            print("No new tracks to add - all entries already exist in sheet")
            return

        # Convert new rows to list format for upload
        new_data = new_rows.values.tolist()

        # Append new rows
        for row in new_data:
            self.worksheet.append_row(row)

        print(f"Successfully added {len(new_data)} new tracks to Google Sheets!")


def main():
    # credentials
    CLIENT_ID = 'f3220ed6bd044024a121a5d2634c538b'
    CLIENT_SECRET = 'b466791b5cb04e63a13ae6ff4fa8980a'
    REDIRECT_URI = 'http://localhost:8888/callback'
    SHEET_ID = '1q-HSQ8qR1UjLvpfF-xSO_tIW_6Ohtjear9vWHlTU0CI'

    # Before creating logger, try to remove the cache file
    import os
    try:
        if os.path.exists(".spotify_cache"):
            os.remove(".spotify_cache")
            print("Removed old cache file")
    except Exception as e:
        print(f"Error removing cache file: {str(e)}")

    logger = SpotifyLogger(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SHEET_ID)
    if logger.sp:
        print("Fetching recent tracks...")
        df = logger.get_recent_tracks(limit=50)

        if df is not None:
            print("\nDataFrame Info:")
            print(df.info())

            print("\nSample of collected data:")
            print(df.head())

            logger.push_to_google_sheets(df)


if __name__ == "__main__":
    main()
