from datetime import timedelta
import os
from src.video import Video
from googleapiclient.discovery import build
import isodate


class PlayList:
    api_key: str = os.environ.get('YT_API_KEY')

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=PlayList.api_key)

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.__info = self.get_service().playlists().list(id=playlist_id, part='contentDetails, snippet',
                                                          maxResults=50, ).execute()
        self.__item_info = self.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                   maxResults=50, ).execute()
        self.title = self.__info["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    @property
    def total_duration(self):
        total_duration = timedelta()
        for item in self.__item_info["items"]:
            video = Video(item["contentDetails"]["videoId"])
            duration = isodate.parse_duration(video.duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        max_likes = 0
        best_link = ""
        for item in self.__item_info["items"]:
            video = Video(item["contentDetails"]["videoId"])
            if int(video.like_count) > max_likes:
                max_likes = int(video.like_count)
                best_link = video.link
        return best_link


