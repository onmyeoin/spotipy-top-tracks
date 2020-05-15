import sys
import spotipy
import spotipy.util as util

username = ''

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)
sp = spotipy.Spotify(auth=token)
sp.trace = False

def create_new_playlist(playlist_name):
    sp.user_playlist_create(username, playlist_name)

def add_tracks(tracks,playlist_name):
    create_new_playlist(playlist_name)
    res = sp.user_playlists(username)
    playlist_info = res['items'][0]
    pid = playlist_info['id']
    sp.user_playlist_add_tracks(username, pid, tracks, position=None)
    print('done')

def top_track(uri,playlist_name):
    top_tracks = []
    for artist in uri:
        res = sp.artist_top_tracks(artist)
        top_tracks.append(res['tracks'][0]['id'])
    add_tracks(top_tracks,playlist_name)

def playlist_tracks(tracks,playlist_name):
    artist_uri = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        artist_uri.append(track['artists'][0]['uri'])
    artist_uri = set(artist_uri)
    top_track(artist_uri,playlist_name)

def show_playlist(playlist_num,playlist_name):
    res = sp.user_playlists(username)
    playlist_info = res['items'][playlist_num]
    playlist_id = sp.playlist(playlist_info['id'])
    tracks = playlist_id['tracks']
    playlist_tracks(tracks,playlist_name)

def main():
    res = sp.user_playlists(username)
    for i, playlist in enumerate(res['items']):
        print("%d %s" % (i, playlist['name']))
    playlist_num = int(input('please select playlist number: '))
    playlist_name = res['items'][playlist_num]['name']
    playlist_name = str(f'{playlist_name} Top Tracks')
    show_playlist(playlist_num,playlist_name)

if __name__ == '__main__':
    main()
