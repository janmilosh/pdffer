import unittest
import requests
import pdb

import bs4

from app.get_links import FormLinks


class ExpressScriptsLinksTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        url = 'https://www.express-scripts.com/services/physicians/medcopa/index.shtml'
        cls.response = FormLinks._get_links_page(url)
        cls.soup_object = None

    def test_makes_successful_get_request_to_express_scripts(cls):
        cls.assertEqual(cls.response.status_code, 200)

    def test_get_request_returns_a_webpage(cls):
        cls.assertIn(b'!DOCTYPE html', cls.response.content)

    def test_make_soup_from_page(cls):
        cls.soup_object = FormLinks._make_soup(cls.response.text)
        cls.assertIsInstance(cls.soup_object, bs4.BeautifulSoup)

    def test_find_links_in_soup(cls):
        link_list = FormLinks._parse_soup(cls.soup_object)
        cls.assertTrue(len(links_list) > 0)
        for link in link_list:
            cls.assertTrue(link[0:4] == 'http')


if __name__ == '__main__':
    unittest.main()