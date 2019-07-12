# Ben Humphrey
# github.com/cxmplex

import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.reader import get_config

YOUTUBE_API_SERVICE_NAME = get_config("youtube", "YOUTUBE_API_SERVICE_NAME")
YOUTUBE_API_VERSION = get_config("youtube", "YOUTUBE_API_VERSION")
YOUTUBE_URL = get_config("youtube", "YOUTUBE_URL")


class YoutubeAPIError(Exception):
    pass


class Youtube:
    _videos = {}

    def __init__(self, key):
        self.yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=key)
        # regex validation filter terms
        # plain text query terms
        self.filterTerms = {
            "KEXP": [
                r"(?i)KEXP.+?Full[\s\W]+?Performance",
                r"(?i)Full[\s\W]+?Performance.+?KEXP.+?",
            ],
            "KCRW": [r"(?i)KCRW"],
            "NPR tiny desk": [r"(?i)NPR.+?Tiny\s+Desk"],
        }

    @property
    def videos(self):
        return self._videos

    def search(self, query):
        for term, filters in self.filterTerms.items():
            try:
                response = (
                    self.yt.search()
                        .list(
                        q="{} {}".format(query, term), part="id,snippet", maxResults=10
                    )
                        .execute()
                )
            except HttpError as e:
                raise (YoutubeAPIError(str(e)))
            # iterate response items
            for result in response.get("items", []):
                if result["id"]["kind"] == "youtube#video":
                    for filter_ in filters:
                        if re.search(filter_, result["snippet"]["title"]) and re.search(
                                query, result["snippet"]["title"]
                        ):
                            if not result["id"]["videoId"] in self._videos:
                                self._videos[
                                    YOUTUBE_URL.format(result["id"]["videoId"])
                                ] = result["snippet"]["title"]
