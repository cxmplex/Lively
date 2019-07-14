# -*- coding: utf-8 -*-
# Ben Humphrey
# github.com/cxmplex

import json

from flask import Flask, request, abort

from config.reader import get_config
from connectors.lastfm import LastFm, LastFmAPIError
from connectors.youtube import Youtube, YoutubeAPIError

app = Flask(__name__)

DEVELOPER_KEYS = get_config("youtube", "API_KEYS")


@app.route("/get_videos", methods=["POST"])
def get_videos():
    if not request.json:
        abort(400)

    key = DEVELOPER_KEYS[0]
    DEVELOPER_KEYS.remove(key)

    data = request.json
    fm = LastFm()
    yt = Youtube(key)

    artists = None
    try:
        artists = fm.get_top_x(data["user"], "artists", 50)
    except LastFmAPIError as e:
        print(str(e))
        abort(503)

    if not artists:
        abort(503)

    for artist in artists:
        try:
            yt.search(artist)
        except YoutubeAPIError:
            # WHY: Youtube has a dumb quota system, each search is 100 quota out of 10,000 maximum
            key = DEVELOPER_KEYS[0]
            DEVELOPER_KEYS.remove(key)
            yt = Youtube(key)
            yt.search(artist)

    return json.dumps(yt.videos)


@app.route("/create_playlist", methods=["POST"])
def create_playlist():
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
