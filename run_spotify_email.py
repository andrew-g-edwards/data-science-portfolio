import os
import logging
from datetime import datetime
import sys
from spotify_analysis import SpotifyAnalyzer
from email_scheduler import SpotifyEmailReporter

# logging set up
log_dir = os.path.expanduser('~/spotify_emailer/logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/spotify_email_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)


def main():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # change directory to check relative paths
        os.chdir(script_dir)

        logging.info("Starting Spotify email report generation")

        # initialize objects
        analyzer = SpotifyAnalyzer()
        analyzer.load_data()
        logging.info("Data loaded successfully")

        # get previous week
        analyzer.get_previous_week_data()
        logging.info("Previous week's data processed")

        # intialize reporter + send email
        reporter = SpotifyEmailReporter(analyzer)
        reporter.send_email()
        logging.info("Email sent successfully")

    except Exception as e:
        logging.error(f"Error running Spotify email report: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()