# Webscraping script for mp3-red.co v2
# Created with love on Python
# Updated Feb 18 2019

import requests
import urllib
from bs4 import BeautifulSoup
import re

page_number = 1
def scrape_mp3 ():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    user_search_text = input("Which Artist would you like to search for?")
    data = {'str':user_search_text}
    try:
        ses=requests.session()
        ses.headers.update(headers)
        r = ses.post('http://mp3-red.co/Search',params=data)
        url = 'http://mp3-red.co'

        #print(ses.cookies.get_dict())
        #print(ses.headers)

        soup = url_page_info(r)
        soup_run(url,soup,ses)
    except ConnectionError:
       print("Error in connecting, check your internet connection!!!")

def url_page_info(r):
    source_code = r
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html.parser")
    return soup

def soup_run(url,soup,ses):
    for get_a_song in soup.findAll('a',{'class':'track-title'}):
        song_name = get_a_song.string
        print(song_name)
        href = url + get_a_song.get('href')
        print(href)
        get_single_item_data(href,url,ses)
    get_next_page(soup, url,ses)

def get_next_page(soup,url,ses):
    global page_number
    page_number += 1
    try:
        next_page = soup.find('a',text='Next page').get('href')
        href = url + next_page
        print("Page", page_number,":", href)
        r = ses.get(href)
        soup_np = url_page_info(r)
        soup_run(url,soup_np,ses)
    except:
        print("---------------------------\n End of Scraping for the Search Item")

def get_single_item_data(item_url,url,ses):
    """
	Get a single page links for specified search item
    """
    source_code = ses.get(item_url)
    plain_text = source_code.text
    #print(plain_text)
    soup = BeautifulSoup(plain_text, "html.parser")
    get_the_song = soup.find('a', {'id': 'download_link'})
    song_link = url + get_the_song.get('href')
    print(song_link)

    r = ses.get(song_link)
    print(r.status_code)
    
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    filename = filename.replace('"', "")
    print("downloading...", filename)
    open(filename, 'wb').write(r.content)
    print("Successfully downloaded", filename)

    ## Testing a single file..
    # with open("burna.mp3", "wb") as code:
    #     code.write(r.content)
               #response = urllib.urlopen("http://mp3-red.co/stream/20781389/burna-boy-bad-boy-feat-korkormikor.mp3")
    #mp3 = response.read()
    #open("burn2", 'wb').write(r)


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
    """
	Not used
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

scrape_mp3()
