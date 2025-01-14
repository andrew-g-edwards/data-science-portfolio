from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from typing import Optional
from datetime import datetime
from spotify_analysis import SpotifyAnalyzer


class SpotifyEmailReporter:
    def __init__(self, analyzer, config_file='.env.yaml'):
        """Initialize email reporter with SpotifyAnalyzer instance and config"""
        self.analyzer = analyzer
        self.smtp_settings = self._load_config(config_file)

    def _load_config(self, config_file: str) -> dict:
        """Load SMTP configuration from env file"""
        config = {}
        with open(config_file, 'r') as file:
            for line in file:
                if ':' in line and not line.strip().startswith('#'):
                    key, value = line.split(':', 1)
                    config[key.strip()] = value.strip().strip("'").strip('"')

        smtp_settings = {
            'sender_email': config.get('SENDER_EMAIL'),
            'sender_password': config.get('SENDER_PASSWORD'),
            'smtp_server': config.get('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(config.get('SMTP_PORT', '465')),
            'recipient_email': config.get('RECIPIENT_EMAIL')
        }

        required_fields = ['sender_email', 'sender_password', 'recipient_email']
        missing_fields = [k for k in required_fields if not smtp_settings.get(k)]
        if missing_fields:
            raise ValueError(f"Missing required config fields: {', '.join(missing_fields)}")

        return smtp_settings

    def send_email(self, subject: Optional[str] = None) -> None:
        """Send email with the Spotify analysis report"""
        if not self._validate_email(self.smtp_settings['sender_email']):
            raise ValueError(f"Invalid sender email: {self.smtp_settings['sender_email']}")
        if not self._validate_email(self.smtp_settings['recipient_email']):
            raise ValueError(f"Invalid recipient email: {self.smtp_settings['recipient_email']}")

        if subject is None:
            subject = f"Your Weekly Spotify Report - {datetime.now().strftime('%B %d, %Y')}"

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.smtp_settings['sender_email']
        msg['To'] = self.smtp_settings['recipient_email']

        html_content = self.generate_email_html()
        msg.attach(MIMEText(html_content, 'html'))

        try:
            with smtplib.SMTP_SSL(self.smtp_settings['smtp_server'],
                                  self.smtp_settings['smtp_port']) as server:
                server.login(self.smtp_settings['sender_email'],
                             self.smtp_settings['sender_password'])
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")

    def _validate_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def create_heatmap_image(self, heatmap_data) -> str:
        """Create heatmap visualization and return as base64 string"""
        cell_width = 40
        cell_height = 40
        margin_left = 120
        margin_top = 60
        padding = 30
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = [f"{i:02d}:00" for i in range(24)]

        width = margin_left + (cell_width * 24) + padding
        height = margin_top + (cell_height * 7) + padding
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)

        try:
            label_font = ImageFont.truetype("Arial.ttf", 14)
            number_font = ImageFont.truetype("Arial.ttf", 11)
        except:
            label_font = number_font = ImageFont.load_default()

        max_val = max(max(row) for row in heatmap_data)

        # draw cells
        for day_idx, day_data in enumerate(heatmap_data):
            for hour_idx, value in enumerate(day_data):
                intensity = value / max_val if max_val > 0 else 0
                if intensity == 0:
                    color = (248, 250, 248)
                else:
                    r = int(248 - (intensity * 180))
                    g = int(250 - (intensity * 100))
                    b = int(248 - (intensity * 180))
                    color = (r, g, b)

                x = margin_left + (hour_idx * cell_width)
                y = margin_top + (day_idx * cell_height)

                draw.rectangle(
                    [x, y, x + cell_width - 1, y + cell_height - 1],
                    fill=color,
                    outline=(238, 238, 238)
                )

                if value > (max_val * 0.2):
                    text = str(int(value))
                    text_bbox = draw.textbbox((0, 0), text, font=number_font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    text_x = x + (cell_width - text_width) // 2
                    text_y = y + (cell_height - text_height) // 2
                    text_color = 'white' if intensity > 0.5 else (60, 60, 60)
                    draw.text((text_x, text_y), text, fill=text_color, font=number_font)

        # draw labels
        for idx, day in enumerate(days):
            y = margin_top + (idx * cell_height) + (cell_height // 2)
            text_bbox = draw.textbbox((0, 0), day, font=label_font)
            text_width = text_bbox[2] - text_bbox[0]
            draw.text((margin_left - text_width - 15, y - 8), day,
                      fill=(60, 60, 60), font=label_font)

        for idx, hour in enumerate(hours):
            if idx % 2 == 0:
                x = margin_left + (idx * cell_width) + (cell_width // 2)
                draw.text((x, margin_top - 20), hour,
                          fill=(60, 60, 60), font=label_font, anchor="ms")

        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()

    def generate_email_html(self) -> str:
        """Generate HTML email content using analyzer data"""

        self.analyzer.load_data()
        self.analyzer.get_previous_week_data()

        stats = self.analyzer.get_basic_stats()
        patterns = self.analyzer.get_listening_patterns()
        comparison = self.analyzer.get_weekly_comparison()
        heatmap_data = self.analyzer.prepare_visualization_data()

        week_start = self.analyzer.weekly_data['played_at'].min()
        week_end = self.analyzer.weekly_data['played_at'].max()

        # generate heatmap image
        heatmap_base64 = self.create_heatmap_image(heatmap_data)

        # top artists + track data
        top_artists = self.analyzer.top_artists()
        top_artists_rows = '\n'.join([
            f"<tr><td>{artist}</td><td>{count}</td></tr>"
            for artist, count in top_artists.items()
        ])

        top_tracks = self.analyzer.weekly_data.groupby(['track_name', 'artist_name'])['played_at'].count()
        top_tracks_sorted = top_tracks.sort_values(ascending=False).head(5)
        top_tracks_rows = '\n'.join([
            f"<tr><td>{track[0]}</td><td>{track[1]}</td><td>{count}</td></tr>"
            for track, count in top_tracks_sorted.items()
        ])

        # comparison data
        if comparison:
            time_change = comparison['listening_time_change']
            time_change_class = 'positive' if time_change >= 0 else 'negative'
            time_change_display = f"+{time_change:.1f}m" if time_change >= 0 else f"{time_change:.1f}m"

            track_change = comparison['track_count_change']
            track_change_class = 'positive' if track_change >= 0 else 'negative'
            track_change_display = f"+{track_change}" if track_change > 0 else f"{track_change}"
        else:
            time_change_display = "N/A"
            track_change_display = "N/A"
            time_change_class = track_change_class = ''

        # email html template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Your Weekly Spotify Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding: 20px;
                    background-color: #1DB954;
                    color: white;
                    border-radius: 8px;
                }}
                .section {{
                    margin-bottom: 30px;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                }}
                .stat-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin-bottom: 20px;
                }}
                .stat-item {{
                    padding: 15px;
                    background-color: white;
                    border-radius: 4px;
                    text-align: center;
                }}
                .value {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #1DB954;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                .comparison {{
                    display: inline-block;
                    padding: 3px 8px;
                    border-radius: 4px;
                    font-size: 14px;
                }}
                .positive {{
                    background-color: #e3fcef;
                    color: #0e7c3f;
                }}
                .negative {{
                    background-color: #fee7e7;
                    color: #c53030;
                }}
                .heatmap-container {{
                    overflow-x: auto;
                    margin: 20px 0;
                }}
                .pattern-summary {{
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Your Weekly Spotify Report</h1>
                <p>{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}</p>
            </div>

            <div class="section">
                <h2>Listening Overview</h2>
                <div class="stat-grid">
                    <div class="stat-item">
                        <div class="value">{stats['total_tracks']}</div>
                        <div>Tracks Played</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{stats['unique_artists']}</div>
                        <div>Unique Artists</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{stats['total_minutes'] / 60:.1f}</div>
                        <div>Hours of Music</div>
                    </div>
                    <div class="stat-item">
                        <div class="value">{stats['avg_song_duration']:.1f}</div>
                        <div>Avg Minutes/Song</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>Top Artists</h2>
                <table>
                    <tr>
                        <th>Artist</th>
                        <th>Plays</th>
                    </tr>
                    {top_artists_rows}
                </table>
            </div>

            <div class="section">
                <h2>Top Tracks</h2>
                <table>
                    <tr>
                        <th>Track</th>
                        <th>Artist</th>
                        <th>Plays</th>
                    </tr>
                    {top_tracks_rows}
                </table>
            </div>

            <div class="section">
                <h2>Hourly Heatmap</h2>
                <div class="heatmap-container" style="text-align: center;">
                    <img src="data:image/png;base64,{heatmap_base64}" 
                         alt="Weekly listening patterns heatmap" 
                         style="max-width: 100%; height: auto; margin: 0 auto;">
                </div>
            </div>

            <div class="section">
                <h2>Week-over-Week Changes</h2>
                <div class="stat-grid">
                    <div class="stat-item">
                        <div>Listening Time</div>
                        <div class="value">
                            {stats['total_minutes']:.1f}m
                            <span class="comparison {time_change_class}">
                                {time_change_display}
                            </span>
                        </div>
                    </div>
                    <div class="stat-item">
                        <div>Tracks Played</div>
                        <div class="value">
                            {stats['total_tracks']}
                            <span class="comparison {track_change_class}">
                                {track_change_display}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content


def test_email():
    try:
        analyzer = SpotifyAnalyzer()

        # initialize reporter with config file
        reporter = SpotifyEmailReporter(analyzer)

        # send email
        reporter.send_email()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error during email test: {str(e)}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    test_email()