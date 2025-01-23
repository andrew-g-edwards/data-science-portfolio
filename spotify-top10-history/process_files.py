import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import glob


def process_spotify_files(directory_path):
    """
    Process all Spotify JSON history files in the given directory
    and return a DataFrame with play counts by artist and year
    """

    all_records = []

    # get all JSON files in directory
    json_files = glob.glob(f"{directory_path}/Streaming_History_Audio_*.json")

    print(f"Found {len(json_files)} JSON files")  # Debug print

    # process each file
    for file_path in json_files:
        print(f"Processing {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f"Found {len(data)} records in {file_path}")  # Debug print

                # print first record to verify structure
                if len(data) > 0:
                    print("Sample record structure:")
                    print(json.dumps(data[0], indent=2))

                all_records.extend(data)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue

    print(f"Total records collected: {len(all_records)}")

    if len(all_records) == 0:
        raise ValueError("No records found in any files")

    # convert to DataFrame
    df = pd.DataFrame(all_records)

    # print column names to verify
    print("\nColumns in DataFrame:")
    print(df.columns.tolist())

    # extract year from timestamp
    df['year'] = pd.to_datetime(df['ts']).dt.year

    # group by year and artist, count plays
    artist_plays = df.groupby(
        ['year', 'master_metadata_album_artist_name']
    ).size().reset_index(name='play_count')

    # remove null artists
    artist_plays = artist_plays.dropna(subset=['master_metadata_album_artist_name'])

    # get top 10 artists for each year
    top_artists = (artist_plays.sort_values(['year', 'play_count'], ascending=[True, False])
                   .groupby('year')
                   .head(10)
                   .sort_values(['year', 'play_count'], ascending=[True, False]))

    return top_artists


def hex_to_rgba(hex_color, opacity):
    """Convert hex color to rgba with opacity"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:], 16)
    return f'rgba({r}, {g}, {b}, {opacity})'


# define colors for each artist
artist_colors = {
    'The Shins': '#4Ad0E2',
    'Modest Mouse': '#50E3C2',
    'Radiohead': '#B968C7',
    'The Strokes': '#3A7FC1',
    'Cage The Elephant': '#62D2A2',
    'Bright Eyes': '#F4C542',
    'alt-J': '#71E4C8',
    'Broken Bells': '#9B6FD3',
    'Passion Pit': '#3F87CD',
    'Alex G': '#F6A35C',
    'Soccer Mommy': '#E85D52',
    'Death Cab for Cutie': '#6B4E9E',
    'Vampire Weekend': '#48C5A5',
    'Glass Animals': '#845DC8',
    'Pinegrove': '#55cc4A',
    'Hot Mulligan': '#FA9140',
    'Taking Back Sunday': '#D44141',
    'Jimmy Eat World': '#FFD24E',
    'Elliott Smith': '#FF8242',
    'Brand New': '#E3575A',
    'Microwave': '#FFB52E',
    'Tigers Jaw': '#FC7B44',
    'Phoebe Bridgers': '#CB3D3D',
    'Jank': '#FFAA38',
    'Title Fight': '#FF6B47',
    'Joyce Manor': '#D84949',
    'Origami Angel': '#FFAA38',
    'Coheed and Cambria': '#D84949',
    'Flume': '#FF5AAD',
    '100 gecs': '#fa61b3',
    'Ratatat': '#FF70C7',
    'SOPHIE': '#FA4B9E',
    'Young Thug': '#ff2222',
    'The Beatles': '#d1d1d1',
    'blink-182': '#BFBFBF'
}


def create_rank_flow_diagram(nodes_df, flows_df):
    # filter years
    valid_years = list(range(2015, 2025))
    nodes_df = nodes_df[nodes_df['Year'].isin(valid_years)].copy()
    flows_df = flows_df[
        flows_df['Year1'].isin(valid_years) &
        flows_df['Year2'].isin(valid_years)
        ].copy()

    # sort nodes by year and position
    nodes_df = nodes_df.sort_values(['Year', 'Position'])

    # calculate node sizes
    max_plays = nodes_df['Plays'].max()
    min_plays = nodes_df['Plays'].min()

    def scale_node_size(plays):
        # scale between 15 and 40
        return 15 + (plays - min_plays) * (40 - 15) / (max_plays - min_plays)

    # get unique years for x-coordinates
    years = sorted(nodes_df['Year'].unique())
    year_to_x = {year: i * 1.2 for i, year in enumerate(years)}

    # create node data
    node_x = []
    node_y = []
    node_labels = []
    node_colors = []
    node_sizes = []
    node_hover_texts = []

    for _, node in nodes_df.iterrows():
        x = year_to_x[node['Year']]
        y = -(node['Position'] - 1) * 1.1

        node_x.append(x)
        node_y.append(y)
        node_labels.append(node['Artist'])
        node_colors.append(artist_colors[node['Artist']])
        node_sizes.append(scale_node_size(node['Plays']))
        node_hover_texts.append(f"{node['Artist']}<br>Year: {node['Year']}<br>{node['Plays']} plays")

    # create figure
    fig = go.Figure()

    # add flows
    for _, flow in flows_df.iterrows():
        x0 = year_to_x[flow['Year1']]
        x1 = year_to_x[flow['Year2']]
        y0 = -(flow['Position1'] - 1) * 1.1
        y1 = -(flow['Position2'] - 1) * 1.1

        # calculate points for the curved path
        curve_x = []
        curve_y = []

        t = np.linspace(0, 1, 100)
        for i in t:
            # X coordinate - linear interpolation
            x = x0 + (x1 - x0) * i

            # Y coordinate with smooth pipe bends
            if i < 0.2:
                # initial horizontal segment
                y = y0
            elif i > 0.8:
                # final horizontal segment
                y = y1
            else:
                normalized_t = (i - 0.2) / 0.6
                # smooth S-curve shape
                ease = 6 * (normalized_t ** 5) - 15 * (normalized_t ** 4) + 10 * (normalized_t ** 3)
                y = y0 + (y1 - y0) * ease

            curve_x.append(x)
            curve_y.append(y)

        # add flow trace
        fig.add_trace(go.Scatter(
            x=curve_x,
            y=curve_y,
            mode='lines',
            line=dict(
                color=hex_to_rgba(artist_colors[flow["Artist"]], 0.6),
                width=2
            ),
            hoverinfo='none',
            showlegend=False
        ))

    # add nodes
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(color='rgb(50, 50, 50)', width=0),
            opacity=1.0
        ),
        text=node_labels,
        textposition="top center",
        textfont=dict(size=10),
        hovertext=node_hover_texts,
        hoverinfo='text',
        showlegend=False
    ))

    # update layout
    fig.update_layout(
        title="My Top 10 Artists by Year",
        plot_bgcolor='white',
        width=1200,
        height=800,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickmode='array',
            ticktext=years,
            tickvals=[year_to_x[year] for year in years],
            title="Year"
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            tickmode='array',
            ticktext=['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10'],
            tickvals=[i * -1.1 for i in range(10)],
            title="Rank"
        ),
        hovermode='closest'
    )

    return fig


if __name__ == "__main__":
    # read the CSV files
    nodes_df = pd.read_csv('spotify_nodes.csv')
    flows_df = pd.read_csv('spotify_flows.csv')

    # create figure
    fig = create_rank_flow_diagram(nodes_df, flows_df)
    fig.show()
    fig.write_html("spotify_history.html")