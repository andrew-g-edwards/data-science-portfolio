import functions_framework
from spotify_logger import SpotifyLogger
import os


@functions_framework.http
def spotify_logger_function(request):
    """HTTP Cloud Function."""
    try:
        logger = SpotifyLogger(
            client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
            client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.environ.get('SPOTIFY_REDIRECT_URI'),
            sheet_id=os.environ.get('SHEET_ID')
        )

        df = logger.get_recent_tracks(limit=50)
        if df is not None:
            logger.push_to_google_sheets(df)
            return 'Success: Data logged to Google Sheets'
        return 'Error: Unable to fetch tracks'
    except Exception as e:
        return f'Error: {str(e)}'