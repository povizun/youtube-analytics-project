import os
from pathlib import Path
import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.environ.get('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__info = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__title = self.info["items"][0]["snippet"]["title"]
        self.__description = self.info["items"][0]["snippet"]["description"]
        self.__url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.__subscriber_count = self.info["items"][0]["statistics"]["subscriberCount"]
        self.__video_count = self.info["items"][0]["statistics"]["videoCount"]
        self.__view_count = self.info["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def info(self):
        return self.__info

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url

    @property
    def subscriber_count(self):
        return self.__subscriber_count

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.info)

    @classmethod
    def get_service(cls):
        return Channel.youtube

    def to_json(self, file_name):
        data = {"channel_id": self.channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count
                }

        with open(Path(__file__).parent.parent / f"src/{file_name}", "w") as file:
            json.dump(data, file)
