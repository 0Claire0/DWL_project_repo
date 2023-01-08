# Musixmatch API get requests

import requests
from pprint import pprint


def get_lyrics(artist_name, song_name, apikey_musixmatch, apiurl_musixmatch):
    query_string = f'{apiurl_musixmatch}matcher.lyrics.get?&q_track={song_name}&q_artist={artist_name}&apikey={apikey_musixmatch}&format=json&f_has_lyrics=1'
    r = requests.get(query_string)
    pprint(r.text)


def main():
    artist_name = "david guetta"
    song_name = "i'm good (blue)"
    apikey_musixmatch = '1b1821d41b9cb328774a18cdd9fddb27'
    apiurl_musixmatch = 'http://api.musixmatch.com/ws/1.1/'
    get_lyrics(artist_name, song_name, apikey_musixmatch, apiurl_musixmatch)

main()