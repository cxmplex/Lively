# Ben Humphrey
# github.com/cxmplex

import pylast
from config.reader import get_config

LASTFM_API_KEY = get_config('lastfm', 'LASTFM_API_KEY')
LASTFM_API_SECRET = get_config('lastfm', 'LASTFM_API_SECRET')
LASTFM_USERNAME = get_config('lastfm', 'LASTFM_USERNAME')
LASTFM_PASSWORD = get_config('lastfm', 'LASTFM_PASSWORD')


class LastFmAPIError(Exception):
    pass


class LastFm:
    def __init__(self):
        self.lfm = pylast.LastFMNetwork(api_key=LASTFM_API_KEY, api_secret=LASTFM_API_SECRET)

    def get_top_x(self, user, type_, limit):
        lfm_user = self.lfm.get_user(user)
        try:
            if type_ == 'artists':
                return [item[0] for item in lfm_user.get_top_artists(limit=limit)]
            if type_ == 'tracks':
                return [item[0] for item in lfm_user.get_top_tracks(limit=limit)]
            if type_ == 'albums':
                return [item[0] for item in lfm_user.get_top_albums(limit=limit)]
        except Exception as e:
            raise LastFmAPIError(str(e))