import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_title(url):
    html = requests.get(url)
    soup = bs(html.content, 'html.parser')
    title = soup.find('title').text.rstrip(" - YouTube")
    return title

def get_good(url):
    html = requests.get(url)
    soup = bs(html, 'html.parser')
    good = soup.select_one('#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer').text
    return good