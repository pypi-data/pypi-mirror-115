from googleapiclient.discovery import build
from loguru import logger

class YouTubeApi():

	def __init__(self, youtube_api_key:str)->None:
		self.youtube_api_key = youtube_api_key
		self.service = build('youtube', 'v3', developerKey=self.youtube_api_key)


	def Subs(self, idChannel: str = None):

		if self.youtube_api_key is None or self.youtube_api_key == "":
			logger.error("The API key from the YouTube API is not specified.")
		else:
			res = self.service.channels().list(id=idChannel, part='snippet,statistics').execute()
			subs = res["items"][0]["statistics"]["subscriberCount"]
			return int(subs)

	def ViewsChannel(self, idChannel: str = None):
		if self.youtube_api_key is None or self.youtube_api_key == "":
			logger.error("The API key from the YouTube API is not specified.")
		else:
			res = self.service.channels().list(id=idChannel, part='snippet,statistics').execute()
			views = res["items"][0]["statistics"]["viewCount"]
			return int(views)
	
	def DescriptionChannel(self, idChannel: str = None):
		if self.youtube_api_key is None or self.youtube_api_key == "":
			logger.error("The API key from the YouTube API is not specified.")
		else:
			res = self.service.channels().list(id=idChannel, part='snippet,statistics').execute()
			desc = res["items"][0]["snippet"]["description"]
			return desc


	def ViewsVideo(self, idVideo: str = None):
		if self.youtube_api_key is None or self.youtube_api_key == "":
			logger.error("The API key from the YouTube API is not specified.")
		else:
			r = self.service.videos().list(id=idVideo, part='statistics').execute()
			views = r["items"][0]["statistics"]["viewCount"]
			return int(views)

	def TitleVideo(self, idVideo: str = None):
		if self.youtube_api_key is None or self.youtube_api_key == "":
			logger.error("The API key from the YouTube API is not specified.")
		else:
			r = self.service.videos().list(id=idVideo, part='snippet').execute()
			title = r["items"][0]["snippet"]["title"]
			return title
	

	def DescriptionVideo(self, idVideo: str = None):
		if self.youtube_api_key is None or self.youtube_api_key == "":
			logger.error("The API key from the YouTube API is not specified.")
		else:
			r = self.service.videos().list(id=idVideo, part='snippet').execute()
			title = r["items"][0]["snippet"]["description"]
			return title