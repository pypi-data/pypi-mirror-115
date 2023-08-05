import requests
from bs4 import BeautifulSoup as bs

def get_title(url):
    html = requests.get(url)
    soup = bs(html.content, 'html.parser')
    title = soup.find('title').text.rstrip(" - YouTube")
    return title
print(get_title('https://www.youtube.com/watch?v=CFTV399rkpY&ab_channel=JTBCEntertainment'))

def get_views(url):
    html = requests.get(url)
    soup = bs(html.content, 'html.parser')
    views = soup.find('div', {'class': 'watch-view-count'}).text.strip()
    return views