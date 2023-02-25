import requests
from bs4 import BeautifulSoup

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'

# does not execute Javascript
response = requests.get(YOUTUBE_TRENDING_URL)

print('Status Code', response.status_code)

doc = BeautifulSoup(response.text, 'html.parser')

print('Page title:', doc.title.text)

# find all the video divs
video_divs = doc.find_all('div', class_='ytd-video-renderer-wiz')

print(f'Found {len(video_divs)} videos')