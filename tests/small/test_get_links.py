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

    def setUp(self):
        self.fl = FormLinks()
        self.doc_links = self.fl.main()
        self.time_string = self.fl._make_time_string_with_days_offset(550)
        print('The time string is: ', self.time_string)
        
    def test_main_method(self):
        for doc_link in self.doc_links:
            self.assertTrue(doc_link[0:5] == 'docs/' and doc_link[-3:] == 'pdf')

    def test_time_string(self):        
        self.assertTrue(type(self.time_string) == str)
        self.assertTrue(len(self.time_string) == 29)

    def test_make_form_request_to_get_headers(self):
        for link in self.doc_links:
            response = self.fl._get_document(link, 550)
            status_code = response.status_code
            # self.assertTrue(status_code == 200 or status_code == 304)
            # pdb.set_trace()

    





if __name__ == '__main__':
    unittest.main()