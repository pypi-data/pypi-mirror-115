import requests
import urllib.parse
import json
import re
from bs4 import BeautifulSoup

def imageSearch(query, max_results=100): 
    """
    Search on Google Images with requests module and scrapes via BeautifulSoup, returning 100 results in an array (if max_results is not set).\n
    :params query: The query string to search for images with.\n
    :max_results (optional): The maximum number of results to return. [from 1 to 100]\n
    :return: A list of images.
    """

    im = [] 
    for script in BeautifulSoup(requests.get(f'https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch', headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}).text, 'html.parser').find_all('script'):
        if script.text.find('AF_initDataCallback') != -1:
            if arr := re.findall('(?<=data:\[)(.*)(?=\])', script.text):
                if arr[0] == '':
                    continue
                im = json.loads(f"[{arr[0]}]")[31][0][12][2]
                break

    def _parsedata_(d):
        if d[1] and d[1][3] and d[1][3][0]:
            return {
                    "image_url": d[1][3][0],
                    "dimensions": (d[1][3][1], d[1][3][2]),
                    "url": d[1][9]["2003"][2],
                    "description": d[1][9]["2003"][3],
                    "url_domain": d[1][9]["183836587"][0],
                }
    
    im = [im for im in list(map(_parsedata_ ,im)) if im]
    if max_results != 100:
        if max_results > 100:
            max_results = 100
        elif max_results < 1:
            max_results = 1
        im = im[:max_results]
    return im