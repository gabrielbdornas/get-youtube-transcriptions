from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from utils import get_formated_today
import stringcase

def get_transcripts(video_id):
	transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
	for transcript in transcript_list:
		file_name = build_file_name(video_id)
		import ipdb; ipdb.set_trace(context=10)

def build_file_name(video_id):
	today = get_formated_today()
	video_title = format_video_title(get_video_title(video_id))
	name = f'{today}_{video_id}_{video_title}.txt'
	return name

def get_video_title(video_id):
	title = YouTube(f'https://youtube.com/watch?v={video_id}')
	title = title.streams[0].default_filename
	return title

def format_video_title(title):
	title = stringcase.snakecase(title)
	return title

get_transcripts('II7UCUbxOus')
