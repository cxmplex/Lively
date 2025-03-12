

from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

from config.reader import get_config


class SpotifyAPIError(Exception):
    pass


class SpotifyAPI:
    def __init__(self):
        credentials = SpotifyClientCredentials(get_config("spotify", "CLIENT_ID"),
                                               get_config("spotify", "CLIENT_SECRET"))
        self.sp = Spotify(client_credentials_manager=credentials)

    def get_playlist(self, user: str, playlist: str, ignores: list) -> list:
        artists = {}
        try:
            res = self.sp.user_playlist(user, playlist)
            while res:
                try:
                    tracks = res['tracks']
                except KeyError:
                    break
                for i, item in enumerate(tracks['items']):
                    track = item['track']
                    artist = track['artists'][0]['name']
                    if artist and artist not in ignores:
                        artists[(track['artists'][0]['name'])] = 1
                if tracks['next']:
                    res = self.sp.next(tracks)
        except SpotifyException as e:
            raise SpotifyAPIError(str(e))
        return list(artists.keys())
