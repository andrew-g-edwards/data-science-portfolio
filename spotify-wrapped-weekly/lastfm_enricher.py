from typing import Dict, Any, List
import pylast
import gspread
from google.oauth2 import service_account
from datetime import datetime
import time
import os
import json


class LastFMEnricher:
    def __init__(self, api_key: str, api_secret: str,
                 google_credentials: Dict[str, Any], sheet_id: str):
        """
        Initialize LastFM enricher

        Args:
            api_key: Last.fm API key
            api_secret: Last.fm API secret
            google_credentials: Google service account credentials dictionary
            sheet_id: Google Sheet ID
        """
        # Initialize Last.fm network
        self.network = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=api_secret
        )

        # Initialize Google Sheets
        credentials = service_account.Credentials.from_service_account_info(
            google_credentials,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        gc = gspread.authorize(credentials)
        self.sheet = gc.open_by_key(sheet_id)

        # Try to get enriched worksheet, create if doesn't exist
        try:
            self.enriched_worksheet = self.sheet.worksheet("enriched_data")
        except gspread.WorksheetNotFound:
            self.enriched_worksheet = self.sheet.add_worksheet(
                title="enriched_data",
                rows=1000,
                cols=30
            )
            self._initialize_enriched_headers()

    def _initialize_enriched_headers(self):
        """Initialize headers for the enriched data worksheet"""
        # Get original headers
        original_headers = self.sheet.sheet1.row_values(1)

        # Add Last.fm specific headers
        lastfm_headers = [
            'lastfm_tags',  # Track-specific tags
            'lastfm_genres',  # Artist-level genres
            'lastfm_categories',  # Combined unique tags and genres
            'album_art_url',  # Album artwork URL
            'lastfm_listeners',  # Track listener count
            'lastfm_playcount',  # Track play count
            'lastfm_sync_time'  # When this data was fetched
        ]

        # Combine headers
        all_headers = original_headers + lastfm_headers
        self.enriched_worksheet.insert_row(all_headers, 1)

    def _enrich_track(self, track_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich a single track with Last.fm data"""
        try:
            print(f"\nFetching Last.fm data for: {track_data['artist_name']} - {track_data['track_name']}")

            track = self.network.get_track(
                track_data['artist_name'],
                track_data['track_name']
            )

            # Get track tags
            print("Getting track tags...")
            try:
                tags = track.get_top_tags(limit=5)
                tag_names = [tag.item.get_name() for tag in tags]
                print(f"Tags found: {tag_names}")
            except Exception as e:
                print(f"Error getting tags: {str(e)}")
                tag_names = []

            # Get artist genres
            print("Getting artist genres...")
            try:
                artist = self.network.get_artist(track_data['artist_name'])
                artist_tags = artist.get_top_tags(limit=3)
                genre_names = [tag.item.get_name() for tag in artist_tags]
                print(f"Artist genres found: {genre_names}")
            except Exception as e:
                print(f"Error getting artist genres: {str(e)}")
                genre_names = []

            # Get track playcount and listeners
            try:
                playcount = track.get_playcount()
                listeners = track.get_listener_count()
            except:
                playcount = ''
                listeners = ''

            # Get album art (if available)
            try:
                album = track.get_album()
                if album:
                    album_art = album.get_cover_image()
                else:
                    album_art = ''
            except:
                album_art = ''

            # Enrich data
            track_data.update({
                'lastfm_tags': '|'.join(tag_names),
                'lastfm_genres': '|'.join(genre_names),  # Artist genres
                'lastfm_categories': '|'.join(set(genre_names + tag_names)),  # Combined unique tags and genres
                'album_art_url': album_art,
                'lastfm_listeners': str(listeners) if listeners else '',
                'lastfm_playcount': str(playcount) if playcount else '',
                'lastfm_sync_time': datetime.now().isoformat()
            })

            # Rate limiting
            time.sleep(0.25)  # 4 requests per second should be safe

        except Exception as e:
            print(f"\nError enriching {track_data['track_name']}: {str(e)}")
            print(f"Full error details: {type(e).__name__}: {str(e)}")
            # Fill with empty values if enrichment fails
            track_data.update({
                'lastfm_tags': '',
                'lastfm_genres': '',
                'album_art_url': '',
                'lastfm_listeners': '',
                'lastfm_playcount': '',
                'lastfm_sync_time': ''
            })

        print(f"Enriched data: {track_data}")
        return track_data

    def _get_all_records(self, worksheet) -> List[Dict[str, Any]]:
        """Get all records from a worksheet and convert to list of dicts"""
        data = worksheet.get_all_records()
        return data

    def sync_data(self, limit=None):
        """Sync data from original sheet to enriched sheet

        Args:
            limit (int, optional): Limit number of records to process for testing
        """
        # Get all data from original sheet
        original_data = self._get_all_records(self.sheet.sheet1)

        # Get existing enriched data
        try:
            enriched_data = self._get_all_records(self.enriched_worksheet)
        except:
            enriched_data = []

        # Find records that need enrichment
        existing_timestamps = {record['timestamp'] for record in enriched_data} if enriched_data else set()
        new_records = [record for record in original_data if record['timestamp'] not in existing_timestamps]

        if limit:
            new_records = new_records[:limit]
            print(f"Limited to processing {limit} records for testing")

        print(f"Enriching {len(new_records)} new records...")

        # Enrich new records
        enriched_records = []
        for record in new_records:
            enriched_record = self._enrich_track(record)
            enriched_records.append(enriched_record)

        # Convert records to list of lists for Google Sheets
        headers = self.enriched_worksheet.row_values(1)
        new_values = [
            [str(record.get(header, '')) for header in headers]
            for record in enriched_records
        ]

        # Append to worksheet
        self.enriched_worksheet.append_rows(new_values)
        print(f"Successfully enriched {len(new_records)} records")


def _load_credentials(env_file='.env.yaml'):
    """Load credentials from environment file"""
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

        # get Last.fm credentials
        lastfm_key_line = [line for line in content.split('\n') if 'LASTFM_API_KEY:' in line][0]
        lastfm_secret_line = [line for line in content.split('\n') if 'LASTFM_API_SECRET:' in line][0]

        lastfm_key = lastfm_key_line.split('LASTFM_API_KEY:')[1].strip().strip('"').strip("'")
        lastfm_secret = lastfm_secret_line.split('LASTFM_API_SECRET:')[1].strip().strip('"').strip("'")

        return {
            'credentials_dict': credentials_dict,
            'sheet_id': sheet_id,
            'lastfm_key': lastfm_key,
            'lastfm_secret': lastfm_secret
        }


def main():
    # Load credentials from .env.yaml
    creds = _load_credentials()

    enricher = LastFMEnricher(
        api_key=creds['lastfm_key'],
        api_secret=creds['lastfm_secret'],
        google_credentials=creds['credentials_dict'],
        sheet_id=creds['sheet_id']
    )

    # Process only 5 tracks for testing
    enricher.sync_data(limit=300)


if __name__ == "__main__":
    main()