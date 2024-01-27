import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.environ.get('YT_API_KEY')

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=Video.api_key)

    def __init__(self, video_id):
        try:
            self.__video_id = video_id
            self.__info = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                           id=video_id
                                                           ).execute()
            self.__title = self.__info["items"][0]["snippet"]["title"]
            self.__link = f"https://youtu.be/{self.__video_id}"
            self.__view_count = self.__info["items"][0]["statistics"]["viewCount"]
            self.__like_count = self.__info["items"][0]["statistics"]["likeCount"]
            self.__duration = self.__info["items"][0]["contentDetails"]["duration"]
        except IndexError:
            self.__video_id = video_id
            self.__info = None
            self.__title = None
            self.__link = None
            self.__view_count = None
            self.__like_count = None
            self.__duration = None

    def __str__(self):
        return self.title

    @property
    def video_id(self):
        return self.__video_id

    @property
    def info(self):
        return self.__info

    @property
    def title(self):
        return self.__title

    @property
    def link(self):
        return self.__link

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count

    @property
    def duration(self):
        return self.__duration


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
