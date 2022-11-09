import json
import pandas as pd
import spotipy
#from spotify_client_credentials import *
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'id'
client_secret = 'secret'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_track_ids(playlist_id):
    music_id_list = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        music_track = item['track']
        music_id_list.append(music_track['id'])
    return music_id_list

def get_track_data(track_id):
    meta = sp.track(track_id)
    features = sp.audio_features(track_id)

    track_details = {"name": meta['name'], "album": meta['album']['name'],
                     "artist": meta['album']['artists'][0]['name'],
                     "release_date": meta['album']['release_date'],
                     "duration_mins": round((meta['duration_ms'] * .001) / 60.0,2),
                     "popularity": meta['popularity'],
                     "energy": features[0]['energy'],
                     "tempo": features[0]['tempo'],
                     "valence": features[0]['valence'],
                     "mode": features[0]['mode'],
                     "danceability": features[0]['danceability']}
    return track_details

playlist_id = '3bgMgB1AdSwXdmLvhnCi6m?si=c48d251edb414215' #christian
#playlist_id = '5DKOMawWrwzashNhgrupFD?si=1914e2fd6be14304' #bobby
#playlist_id = '78K99o2OV4v18XbkVWTUrp?si=0834f2fda0034df1' #andrew

track_ids = get_track_ids(playlist_id)

tracks = []
for i in range(len(track_ids)):
    track = get_track_data(track_ids[i])
    tracks.append(track)

with open('chris_spotify_100.json', 'w') as outfile:
     json.dump(tracks, outfile, indent=4)

df = pd.read_json('chris_spotify_100.json')
df.to_csv('chris_spotify_100.csv', index=None)
