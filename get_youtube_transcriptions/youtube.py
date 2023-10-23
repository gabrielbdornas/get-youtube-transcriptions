from pytube import YouTube
from unidecode import unidecode
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from utils import get_formated_today
import stringcase
import sys

def get_transcripts(video_url):
	video_id = get_video_id(video_url)
	try:
		transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
		file_name = build_file_name(video_id)
		with open(f'transcripts/{file_name}', 'a', encoding='utf-8') as file:
			for transcript in transcript_list:
				formatter = TextFormatter()
				text = transcript.fetch()
				text_formatted = formatter.format_transcript(text)
				file.write(f'- {transcript.language}\n\n')
				file.write(f'- Generated by YouTube: {transcript.is_translatable}\n\n')
				file.write(f'{text_formatted}\n\n')
		print('Transcript generated.')
	except:
		file_name = build_error_file_name(video_id)
		with open(f'transcripts/{file_name}', 'a', encoding='utf-8') as file:
			file.write(f'Video with id {video_id} not found.')
		print('Something went wrong. Check video URL.')

def get_video_id(video_url):
	video_url_split = video_url.split('watch?v=')
	return video_url_split[1][:12]

def build_file_name(video_id):
	today = get_formated_today()
	video_title = format_video_title(get_video_title(video_id))
	video_title = snake_small_case(video_title)
	name = f'{today}_{video_id}_{video_title}.txt'
	return name

def build_error_file_name(video_id):
	today = get_formated_today()
	name = f'{today}_{video_id}_not_found.txt'
	return name

def get_video_title(video_id):
	title = YouTube(f'https://youtube.com/watch?v={video_id}')
	title = title.streams[0].default_filename
	return title

def format_video_title(title):
	title = stringcase.snakecase(title)
	return title

def snake_small_case(name):
	name_lower = name.lower()
	name_unidecode = unidecode(name_lower)
	name_alphanumeric = re.sub('[^A-Za-z0-9]+', ' ', name_unidecode)
	name_split = name_alphanumeric.split(' ')
	name_empty = [x for x in name_split if x != '']
	name = '_'.join(name_empty)
	return name

if __name__ == '__main__':
	get_transcripts(sys.argv[1])
