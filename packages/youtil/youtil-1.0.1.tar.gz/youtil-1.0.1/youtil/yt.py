import requests
from bs4 import BeautifulSoup as bs

def get_title(url):
    html = requests.get(url)
    soup = bs(html.content, 'html.parser')
    title = soup.find('title').text.rstrip(" - YouTube")
    return title

def get_good(url):
    html = requests.get(url)
    soup = bs(html.content, 'html.parser')
    good = soup.find('yt-formatted-string', {'id':'text'}).text
    return good