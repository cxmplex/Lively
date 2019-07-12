# Lively
Finds live performances on Youtube from your favorites artists on Last.Fm


# What this is

This is the back-end to a website that I'm working on. It's a bit sloppy currently, will be refactored once the front-end is done.

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
    "YOUTUBE_URL": "https://youtube.com/watch?v={}"
  }
}

```

I use multiple `projects` in the Google API Dashboard. Google's quota limit is set to 10,000 UNITS. Each (1) search costs 100 UNITS. The solution is to just create multiple projects, as the quota is tracker per project.

# Supported live performance channels

I've only added in the following

* KEXP
* KCRW
* NPR Tiny Desk

Raise an issue if you'd like me to add more.
