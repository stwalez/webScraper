# Webscraping script for mp3-red.co v1
# Created with love on Python
# Jan 1 2019

import requests
import urllib
from bs4 import BeautifulSoup
import re

page_number = 1
def scrape_mp3 ():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    user_search_text = input("Which Artist would you like to search for?")
    data = {'str':user_search_text}
    r = requests.post('http://mp3-red.co/Search',headers=headers, params=data)
    url = 'http://mp3-red.co'
    soup = url_page_info(r)
    soup_run(url,soup,headers)


def url_page_info(r):
    source_code = r
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup

def soup_run(url,soup,headers):
    for get_a_song in soup.findAll('a',{'class':'track-title'}):
        song_name = get_a_song.string
        print(song_name)
        href = url + get_a_song.get('href')
        print(href)
        get_single_item_data(href,url,headers)
    get_next_page(soup, url,headers)

def get_next_page(soup,url,headers):
    global page_number
    page_number += 1
    try:
        next_page = soup.find('a',text='Next page').get('href')
        href = url + next_page
        print("Page", page_number,":", href)
        r = requests.get(href,headers=headers)
        soup_np = url_page_info(r)
        soup_run(url,soup_np,headers)
    except:
        print("---------------------------\n End of Scraping for the Search Item")

def get_single_item_data(item_url,url, headers):
    source_code = requests.get(item_url,headers=headers)

    cookies1 = source_code.headers['Set-Cookie']
    cookies2 = cookies1.split(' ')
    cookies3 = [w.replace(';', '') for w in [x for x in cookies2 if "=" in x]]
    cookies4 = dict(item.split("=") for item in cookies3)

    plain_text = source_code.text
    #print(plain_text)
    soup = BeautifulSoup(plain_text)
    get_the_song = soup.find('a', {'id': 'download_link'})
    song_link = url + get_the_song.get('href')
    print(song_link)

    r = requests.get(song_link, headers=headers,cookies=cookies4)
    print(r.status_code)
    print(r.headers)
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    open(filename, 'wb').write(r.content)

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def is_downloadable(url):

    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

scrape_mp3()
