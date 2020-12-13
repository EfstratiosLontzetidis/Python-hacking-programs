#!usr/bin/env python
import requests, re
import urllib.parse as urlparse
target_url="https://sweetnart.gr/"
#links list to be stored
target_links=[]

def extract_links_from(url):
    #get links
    response=requests.get(url)
    #regex for links
    return  re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

def crawl(url):
    href_links = extract_links_from(url)
    #complete the uncompleted urls
    for link in href_links:
        link = urlparse.urljoin(url, link)
    # split the hrefs starting with #
        if "#" in link:
            link=link.split("#")[0]
    #store unique links
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            #recursive crawl
            crawl(link)

crawl(target_url)

