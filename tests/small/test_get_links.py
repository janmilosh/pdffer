import unittest
import requests

from app.get_links import FormLinks

class ExpressScriptsLinksTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        url = 'https://www.express-scripts.com/services/physicians/medcopa/index.shtml'
        cls.response = FormLinks._get_links(url)

    def test_makes_successful_get_request_to_express_scripts(cls):
        cls.assertEqual(cls.response.status_code, 200)

    def test_get_request_returns_a_webpage(cls):
        cls.assertIn(b'!DOCTYPE html', cls.response.content)

    def test_saves_content_to_pickled_file(cls)
        

if __name__ == '__main__':
    unittest.main()