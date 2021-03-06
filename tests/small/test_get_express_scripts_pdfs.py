import datetime, os, unittest
import requests
import pdb

import bs4

from app.get_express_scripts_pdfs import ExpressScriptsPDF
from app.helpers.universal import Helpers


class ExpressScriptsScrapingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.es = ExpressScriptsPDF()
        cls.helpers = Helpers('pdfs')
        url = os.path.join(cls.es.base_url, cls.es.page_route)
        cls.response = cls.helpers._request_links_page(url)
        cls.soup_object = cls.helpers._make_soup(cls.response.text)

    def test_makes_successful_get_request_to_express_scripts(cls):
        cls.assertEqual(cls.response.status_code, 200)

    def test_get_request_returns_a_webpage(cls):
        cls.assertIn(b'!DOCTYPE html', cls.response.content)

    def test_make_soup_from_page(cls):  
        cls.assertIsInstance(cls.soup_object, bs4.BeautifulSoup)

    def test_find_all_links_in_soup(cls):
        links = cls.helpers._find_all_links_in_soup(cls.soup_object)
        cls.assertTrue(len(links) > 0)
        for link in links:
            cls.assertTrue(type(link) == str)

    def test_find_all_document_links_in_list_of_links(cls):
        doc_links = cls.helpers._return_only_pdf_links(cls.soup_object)
        for doc_link in doc_links:
            cls.assertTrue(doc_link[0:5] == 'docs/' and doc_link[-3:] == 'pdf')


class ExpressScriptsFormRequestsTest(unittest.TestCase):    
    
    @classmethod
    def setUpClass(cls):
        cls.es = ExpressScriptsPDF()
        cls.helpers = Helpers('pdfs')

        url = os.path.join(cls.es.base_url, cls.es.page_route)
        page = cls.helpers._request_links_page(url)
        soup = cls.helpers._make_soup(page.text)
        cls.doc_links =  cls.helpers._return_only_pdf_links(soup)
        
        cls.responses = []

        for link in cls.doc_links:
            response = cls.helpers._request_document(cls.es.base_url, link, 1000)
            cls.responses.append(response)

    def test_prepare_links(cls):
        for doc_link in cls.doc_links:
            cls.assertTrue(doc_link[0:5] == 'docs/' and doc_link[-3:] == 'pdf')

    def test_make_time_string(cls):
        time_string = cls.helpers._make_time_string_with_days_offset(1000)        
        cls.assertTrue(type(time_string) == str)
        cls.assertTrue(len(time_string) == 29)

    def test_make_document_request(cls):
        for response in cls.responses:
            status_code = response.status_code
            cls.assertTrue(status_code == 200 or status_code == 304 or status_code == 404)

    def test_create_dict_for_doc_links(cls):
        docs_dict = cls.es._create_dict_for_doc_links(cls.responses)
        cls.assertIs(type(docs_dict), dict)
        cls.assertGreater(len(docs_dict), 0)

    @unittest.skip('Test of Main method, no need to run this every time.')
    def test_main_method(cls):
        docs_dict = cls.es.main(1000)
        cls.assertIs(type(docs_dict), dict)
        cls.assertGreater(len(docs_dict), 0)


if __name__ == '__main__':
    unittest.main()
