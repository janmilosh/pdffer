import datetime, os, unittest
import requests
import pdb

import bs4

from app.get_links import FormLinks


class ExpressScriptsScrapingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fl = FormLinks()
        url = os.path.join(cls.fl.base_url, cls.fl.page_route)
        cls.response = cls.fl._get_links_page(url)
        cls.soup_object = cls.fl._make_soup(cls.response.text)

    def test_makes_successful_get_request_to_express_scripts(cls):
        cls.assertEqual(cls.response.status_code, 200)

    def test_get_request_returns_a_webpage(cls):
        cls.assertIn(b'!DOCTYPE html', cls.response.content)

    def test_make_soup_from_page(cls):  
        cls.assertIsInstance(cls.soup_object, bs4.BeautifulSoup)

    def test_find_all_links_in_soup(cls):
        links = cls.fl._find_all_links(cls.soup_object)
        cls.assertTrue(len(links) > 0)
        for link in links:
            cls.assertTrue(type(link) == str)

    def test_find_all_document_links_in_list_of_links(cls):
        doc_links = cls.fl._find_all_document_links(cls.soup_object)
        for doc_link in doc_links:
            cls.assertTrue(doc_link[0:5] == 'docs/' and doc_link[-3:] == 'pdf')


class ExpressScriptsFormRequestsTest(unittest.TestCase):    
    
    @classmethod
    def setUp(cls):
        cls.fl = FormLinks()
        cls.doc_links = cls.fl.main()
        cls.time_string = cls.fl._make_time_string_with_days_offset(550)
        cls.responses = []

        for link in cls.doc_links:
            response = cls.fl._make_document_request(link, 1000)
            cls.responses.append(response)
    
    def test_main_method(cls):
        for doc_link in cls.doc_links:
            cls.assertTrue(doc_link[0:5] == 'docs/' and doc_link[-3:] == 'pdf')

    def test_time_string(cls):        
        cls.assertTrue(type(cls.time_string) == str)
        cls.assertTrue(len(cls.time_string) == 29)

    def test_make_form_request_to_get_headers(cls):
        for response in cls.responses:
            status_code = response.status_code
            cls.assertTrue(status_code == 200 or status_code == 304 or status_code == 404)

    def test_create_dict_for_doc_links(cls):
        docs = {}
        for response in cls.responses:
            form_name = response.url.split('/')[-1].split('.')[0]
            try:
                last_modified = response.headers['last-modified']
            except:
                last_modified = ''
            try:
                etag = response.headers['etag']
            except:
                etag = ''

            docs[form_name] = (last_modified, response.url, response.status_code, etag)
            print(form_name, docs[form_name])


if __name__ == '__main__':
    unittest.main()