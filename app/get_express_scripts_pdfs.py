#!/usr/bin/env python
import datetime, os
from contextlib import closing
import pdb 

from bs4 import BeautifulSoup
import requests


class ExpressScriptsPDF:
    def __init__(self):
        self.root_dir = os.getcwd()
        self.pdf_directory_name = 'pdfs'
        self.base_url = 'https://www.express-scripts.com/services/physicians/medcopa'
        self.page_route = 'index.shtml'

    def main(self, offset_in_days):
        url = os.path.join(self.base_url, self.page_route)
        page = self._request_links_page(url)
        soup = self._make_soup(page.text)
        links =  self._return_only_document_links(soup)

        responses = []
        for link in links:
            response = self._request_document(link, offset_in_days)
            responses.append(response)
        docs_dict = self._create_dict_for_doc_links(responses)
        print(docs_dict)
        return docs_dict

    def _request_links_page(self, url):
        return requests.get(url)

    def _make_soup(self, text):
        soup = BeautifulSoup(text)
        return soup

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
    
    def _request_document(self, doc_path, days_offset):
        request_parameters = self._make_request_parameters(doc_path, days_offset)
        
        # Stream=true only pulls headers, not full document
        with closing(requests.get( request_parameters['url'],
                                   stream=True,
                                   headers=request_parameters['headers'])
                                 ) as response:
            
            print('Getting:', request_parameters['url'])

            if response.status_code == requests.codes.not_modified:
                print('Document has not been modified since {0}, {1}'.format(
                                last_modified,response.status_code))
                
            elif response.status_code == requests.codes.ok:
                self._write_content_to_file(response,
                                        request_parameters['url'],
                                        self.pdf_directory_name)
                print('Document was modified on {0}, {1}'.format(
                                response.headers['last-modified'],
                                response.status_code))
            
            else:
                print("There was a {0} error on the response".format(response.status_code))
        return response

    def _make_request_parameters(self, doc_path, days_offset):
        url = os.path.join(self.base_url, doc_path)
        last_modified = self._make_time_string_with_days_offset(days_offset)            
        headers = { 'If-Modified-Since' : last_modified, }
        return { 'url': url, 'headers': headers }

    def _make_time_string_with_days_offset(self, offset_in_days):
        return (datetime.datetime.utcnow() - datetime.timedelta(days=offset_in_days)) \
                    .strftime('%a, %d %b %Y %H:%M:%S GMT')

    def _write_content_to_file(self, response, file_url, pdf_directory_name):
        save_file_path = self._create_save_file_path(file_url, pdf_directory_name)
        with open(save_file_path, 'wb') as save_file:
            for chunk in response.iter_content(1024):
                save_file.write(chunk)

    def _create_save_file_path(self, file_url, pdf_directory_name):
         return os.path.join(self.root_dir,
                             pdf_directory_name,
                             file_url.split('/')[-1]) 

    def _create_dict_for_doc_links(self, responses):
        docs_dict = {}
        for response in responses:
            form_name = response.url.split('/')[-1].split('.')[0]
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

