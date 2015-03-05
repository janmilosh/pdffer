#!/usr/bin/env python
import datetime, os
from contextlib import closing
import pdb 

from bs4 import BeautifulSoup
import requests


class Helpers:
    def __init__(self, pdf_directory_name):
        self.root_dir = os.getcwd()
        self.pdf_directory_name = pdf_directory_name

    def _request_links_page(self, url):
        return requests.get(url)

    def _make_soup(self, text):
        soup = BeautifulSoup(text)
        return soup

    def _request_document(self, base_url, doc_path, days_offset):
        request_parameters = self._make_request_parameters(base_url, doc_path, days_offset)
        
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

    def _make_request_parameters(self, base_url, doc_path, days_offset):
        url = os.path.join(base_url, doc_path)
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
