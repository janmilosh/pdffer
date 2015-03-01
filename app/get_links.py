#!/usr/bin/env python
import datetime, os
from contextlib import closing
import pdb 

from bs4 import BeautifulSoup
import requests


class FormLinks:
    def __init__(self):
        self.root_dir = os.getcwd()
        self.form_links = []
        self.base_url = 'https://www.express-scripts.com/services/physicians/medcopa'
        self.page_route = 'index.shtml'

    def main(self):
        url = os.path.join(self.base_url, self.page_route)
        page = self._get_links_page(url)
        soup = self._make_soup(page.text)
        return self._find_all_document_links(soup)
    
    def _get_links_page(self, url):
        return requests.get(url)

    def _make_soup(self, text):
        soup = BeautifulSoup(text)
        return soup

    def _find_all_links(self, soup):
        all_links = soup.find_all('a')
        hrefs = set()
        for link in all_links:
            link = link.get('href')
            if link != None:
                hrefs.add(link)
        return hrefs

    def _find_all_document_links(self, soup):
        hrefs = self._find_all_links(soup)
        return [href for href in hrefs if href[0:5] == 'docs/']

    def _make_time_string_with_days_offset(self, offset_in_days):
        return (datetime.datetime.utcnow() - datetime.timedelta(days=offset_in_days)) \
                    .strftime('%a, %d %b %Y %H:%M:%S GMT')

    def _make_document_request(self, doc_path, days_offset):
        url = os.path.join(self.base_url, doc_path)
        last_modified = self._make_time_string_with_days_offset(days_offset)
        
        headers = { 'If-Modified-Since' : last_modified, }
 
        # Stream=true only pulls headers, not full document
        with closing(requests.get(url, stream=True, headers=headers)) as response:
            print('Getting:', url)

            if response.status_code == requests.codes.not_modified:
                print('Document has not been modified since {0}, {1}'.format(last_modified,response.status_code))
                
            elif response.status_code == requests.codes.ok:
                with open('doc.pdf', 'wb') as save_file:
                    for chunk in response.iter_content(1024):
                        save_file.write(chunk)
                print('Document was modified on {0}, {1}'.format(response.headers['last-modified'], response.status_code))
            
            else:
                print("There was a {0} error on the response".format(response.status_code))
        return response


if __name__=='__main__':
    self.main()

