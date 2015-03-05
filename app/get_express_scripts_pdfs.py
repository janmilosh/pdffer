#!/usr/bin/env python
import datetime, os
from contextlib import closing
import pdb 

from bs4 import BeautifulSoup
import requests

from app.helpers.universal import Helpers


class ExpressScriptsPDF:
    def __init__(self):
        helpers = Helpers('pdfs')
        self.base_url = 'https://www.express-scripts.com/services/physicians/medcopa'
        self.page_route = 'index.shtml'

    def main(self, offset_in_days):
        url = os.path.join(self.base_url, self.page_route)
        page = helpers._request_links_page(url)
        soup = helpers._make_soup(page.text)
        links =  self._return_only_document_links(soup)

        responses = []
        for link in links:
            response = helpers._request_document(base_url, link, offset_in_days)
            responses.append(response)
        docs_dict = self._create_dict_for_doc_links(responses)
        print(docs_dict)
        return docs_dict    

    def _find_all_links_in_soup(self, soup):
        all_links = soup.find_all('a')
        hrefs = set()
        for link in all_links:
            link = link.get('href')
            if link != None:
                hrefs.add(link)
        return hrefs

    def _return_only_document_links(self, soup):
        hrefs = self._find_all_links_in_soup(soup)
        return [href for href in hrefs if href[0:5] == 'docs/'] 
    
    def _create_form_name(self, response):
        return response.url.split('/')[-1].split('.')[0]

    def _create_dict_for_doc_links(self, responses):
        docs_dict = {}
        for response in responses:
            form_name = self._create_form_name(response)
            try:
                last_modified = response.headers['last-modified']
            except:
                last_modified = ''
            try:
                etag = response.headers['etag'].replace('"', '')
            except:
                etag = ''

            docs_dict[form_name] = (last_modified,
                                    response.url,
                                    response.status_code,
                                    etag)

        return docs_dict


if __name__=='__main__':
    es = ExpressScriptsPDF()
    es.main(1000)

