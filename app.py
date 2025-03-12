
import json

from flask import Flask, request, abort

from config.reader import get_config
from connectors.lastfm import LastFm, LastFmAPIError
from connectors.spotify import SpotifyAPI, SpotifyAPIError
from connectors.youtube import Youtube, YoutubeAPIError

app = Flask(__name__)

DEVELOPER_KEYS = get_config("youtube", "API_KEYS")


@app.route("/get_videos", methods=["POST"])
def get_videos():
    print("Received request for videos")
    if not request.json:
        abort(400)

    key = DEVELOPER_KEYS[0]
    DEVELOPER_KEYS.remove(key)

    data = request.json
    fm = LastFm()
    yt = Youtube(key)

    artists = None
    if data["user"] and not data["playlist"]:
        try:
            artists = fm.get_top_x(data["user"], "artists", get_config("lastfm", "LIMIT"),
                                   get_config("lastfm", "PERIOD"))
        except LastFmAPIError as e:
            print(str(e))
            abort(503)
    if data["playlist"] and data["user"]:
        try:
            sp = SpotifyAPI()
            artists = sp.get_playlist(data["user"], data["playlist"], data["ignore"])
        except SpotifyAPIError as e:
            print(str(e))
            abort(503)
    if not artists:
        print("Didn't find any artists, aborting")
        abort(503)
    # this should be in individual connectors probably like I do above for spotify
    ignores = list(x.lower() for x in data['ignore'])
    for artist in artists:
        if artist.lower() in ignores:
            continue
        should_break = False
        while not should_break:
            try:
                yt.search(artist)
                should_break = True
            except YoutubeAPIError:
                # WHY: Youtube has a dumb quota system, each search is 100 quota out of 10,000 maximum
                key = DEVELOPER_KEYS[0]
                DEVELOPER_KEYS.remove(key)
                yt = Youtube(key)

    return json.dumps(yt.videos)


@app.route("/create_playlist", methods=["POST"])
def create_playlist():
    print("Received request for playlist")
    if not request.json:
        abort(400)
    data = request.json

    yt = Youtube(get_config("youtube", "PLAYLIST_KEY"))
    res = yt.create_playlist(data["items"])

    if not res:
        abort(503)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()
