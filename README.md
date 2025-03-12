# Lively
Finds live performances on Youtube from your favorites artists on Last.Fm


# What this is

This is the back-end to a website that I'm working on. It's a bit sloppy currently, will be refactored once the front-end is done.

- Implements Spotify API, Youtube API, Last FM API

# How to use

Create a config.json with the following information:

```
{
  "lastfm": {
    "LASTFM_USERNAME": "YOUR_USERNAME",
    "LASTFM_PASSWORD": "YOUR_PASSWORD",
    "LASTFM_API_KEY": "YOUR_API_KEY",
    "LASTFM_API_SECRET": "YOUR_API_SECRET"
  },
  "youtube": {
    "API_KEYS": ["key1", "key2", "etc"]
    "YOUTUBE_API_SERVICE_NAME": "youtube",
    "YOUTUBE_API_VERSION": "v3",
    "YOUTUBE_URL": "https://youtube.com/watch?v={}",
    "PLAYLIST_KEY": "",
    "SECRETS": ""
  },
  "spotify": {
      "CLIENT_ID": "",
      "CLIENT_SECRET": ""
  }
}

```

I use multiple `projects` in the Google API Dashboard. Google's quota limit is set to 10,000 UNITS. Each (1) search costs 100 UNITS. The solution is to just create multiple projects, as the quota is tracker per project.

Send a `POST` request to `127.0.0.1:5000/get_videos` with a json body containing the following:

```
{
  "user": "LastFmUsernameYouWantToSearch"
}
```

You'll get back a json of the results.

To change the number of artists looked up, go to app.py and look for this line:

`artists = fm.get_top_x(data['user'], 'artists', 100)`

100 artists will require 400 separate searches. 400 * 100 unit cost = 40,000 Units = 4 separate google projects. I plan on optimizing this in the future.

# Supported live performance channels

I've added in the following

* KEXP
* KCRW
* NPR Tiny Desk
* Like a Version
* Sofar
* Mahogany Sessions
* WFUV
* EQX House Session
* Audiotree
* KXT

Raise an issue if you'd like me to add more.
