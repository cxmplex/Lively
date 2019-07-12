# Ben Humphrey
# github.com/cxmplex

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

from config.reader import get_config


DEVELOPER_KEY = get_config('youtube', 'DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = get_config('youtube', 'YOUTUBE_API_SERVICE_NAME')
YOUTUBE_API_VERSION = get_config('youtube', 'YOUTUBE_API_VERSION')
YOUTUBE_URL = get_config('youtube', 'YOUTUBE_URL')


class YoutubeAPIError(Exception):
    pass


class Youtube:
    def __init__(self):
        self.yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        self.videos = {}
        # regex validation filter terms
        # plain text query terms
        self.filterTerms = {
            'KEXP': [r'(?i)KEXP.+?Full[\s\W]+?Performance', r'(?i)Full[\s\W]+?Performance.+?KEXP.+?'],
            'KCRW': [r'(?i)KCRW'],
            'NPR tiny desk': [r'(?i)NPR.+?Tiny\s+Desk'],
            'like a version': [r'(?i)Like[\s\W]+A[\s\W]+Version']
        }

    def search(self, query):
        for term, filters in self.filterTerms.items():
            try:
                response = self.yt.search().list(
                    q=query + ' ' + term,
                    part='id,snippet',
                    maxResults=10
                ).execute()
            except HttpError as e:
                raise(YoutubeAPIError(str(e)))
            # iterate response items
            for result in response.get('items', []):
                if result['id']['kind'] == 'youtube#video':
                    for filter_ in filters:
                        if re.search(filter_, result['snippet']['title']) and re.search(query, result['snippet']['title']):
                            if not result['id']['videoId'] in self.videos:
                                self.videos[YOUTUBE_URL.format(result['id']['videoId'])] = result['snippet']['title']
        return self.videos
