#!/usr/bin/env python
import os
import pdb 

from bs4 import BeautifulSoup
import requests

class FormLinks:
    def __init__(self):
        self.root_dir = os.getcwd()
        self.form_links = []
    
    def _get_links_page(url):
        return requests.get(url)

    def _make_soup(text):
        soup = BeautifulSoup(text)
        print(soup.prettify())
        pdb.trace()
        return soup



if __name__=='__main__':
	pass
