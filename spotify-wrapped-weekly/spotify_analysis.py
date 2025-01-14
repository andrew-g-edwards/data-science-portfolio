import pandas as pd
import gspread
from google.oauth2 import service_account
import json
import pytz
from datetime import datetime, timedelta


class SpotifyAnalyzer:
    def __init__(self, env_file='.env.yaml'):
        """Initialize analyzer with credentials from environment file"""
        self.credentials = self._load_credentials(env_file)
        self.df = None
        self.weekly_data = None
        self.previous_week_data = None

    def _load_credentials(self, env_file):
        """Load Google Sheets credentials from environment file"""
        with open(env_file, 'r') as file:
            content = file.read()

            # service account info
            start = content.find('GOOGLE_SERVICE_ACCOUNT_INFO: \'') + len('GOOGLE_SERVICE_ACCOUNT_INFO: \'')
            end = content.find('\'', start)
            service_account_str = content[start:end]
            credentials_dict = json.loads(service_account_str)

            # get sheet ID
            sheet_id_line = [line for line in content.split('\n') if 'SHEET_ID:' in line][0]
            sheet_id = sheet_id_line.split('SHEET_ID:')[1].strip().strip('"').strip("'")

            return {
                'credentials_dict': credentials_dict,
                'sheet_id': sheet_id
            }

    def load_data(self):
        """Load and prepare data from Google Sheet"""
        credentials = service_account.Credentials.from_service_account_info(
            self.credentials['credentials_dict'],
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(self.credentials['sheet_id'])

        # load and convert to DataFrame
        data = sheet.worksheet("Sheet1").get_all_records()
        self.df = pd.DataFrame(data)

        # convert to datetime in EST
        eastern = pytz.timezone('America/New_York')
        self.df['played_at'] = pd.to_datetime(self.df['timestamp']).dt.tz_convert(eastern)

        # create fields
        self.df['play_week'] = self.df['played_at'].dt.strftime('%Y-W%V')
        self.df['play_hour'] = self.df['played_at'].dt.hour
        self.df['play_day'] = self.df['played_at'].dt.day_name()

        return self.df

    def get_previous_week_data(self):
        """Get data for the previous week"""
        eastern = pytz.timezone('America/New_York')
        now = datetime.now(eastern)

        # define weeks
        start_of_this_week = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now.weekday())
        end_of_prev_week = start_of_this_week - timedelta(microseconds=1)
        start_of_prev_week = start_of_this_week - timedelta(days=7)

        # filter from previous week
        mask = (self.df['played_at'] >= start_of_prev_week) & (self.df['played_at'] <= end_of_prev_week)
        self.weekly_data = self.df[mask].copy()

        # get previous week
        prev_prev_week_end = start_of_prev_week - timedelta(microseconds=1)
        prev_prev_week_start = start_of_prev_week - timedelta(days=7)
        prev_mask = (self.df['played_at'] >= prev_prev_week_start) & (self.df['played_at'] <= prev_prev_week_end)
        self.previous_week_data = self.df[prev_mask].copy()

        return self.weekly_data

    def get_basic_stats(self):
        """Get basic listening statistics"""
        return {
            'total_tracks': len(self.weekly_data),
            'unique_artists': self.weekly_data['artist_name'].nunique(),
            'unique_songs': self.weekly_data['track_name'].nunique(),
            'total_minutes': (self.weekly_data['duration_ms'].sum() / 60000).round(2),
            'avg_song_duration': (self.weekly_data['duration_ms'].mean() / 60000).round(2)
        }

    def top_artists(self, n=5):
        """Get top artists for the week"""
        return self.weekly_data['artist_name'].value_counts().head(n)

    def get_listening_patterns(self):
        """Analyze listening patterns by day and hour"""
        return {
            'daily_counts': self.weekly_data['play_day'].value_counts().to_dict(),
            'hourly_counts': self.weekly_data['play_hour'].value_counts().sort_index().to_dict()
        }

    def get_weekly_comparison(self):
        """Compare current week with previous week"""
        if self.previous_week_data is None:
            return None

        current_stats = self.get_basic_stats()

        temp = self.weekly_data
        self.weekly_data = self.previous_week_data
        previous_stats = self.get_basic_stats()
        self.weekly_data = temp

        return {
            'listening_time_change': current_stats['total_minutes'] - previous_stats['total_minutes'],
            'track_count_change': current_stats['total_tracks'] - previous_stats['total_tracks']
        }

    def prepare_visualization_data(self):
        """Prepare data for listening patterns heatmap"""
        if self.weekly_data is None:
            raise ValueError("No weekly data loaded. Please run get_weekly_data() first.")

        day_map = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
            'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }

        heatmap_data = []
        for day in range(7):
            day_data = []
            for hour in range(24):
                count = len(self.weekly_data[
                                (self.weekly_data['play_day'].map(day_map) == day) &
                                (self.weekly_data['play_hour'] == hour)
                                ])
                day_data.append(count)
            heatmap_data.append(day_data)

        return heatmap_data