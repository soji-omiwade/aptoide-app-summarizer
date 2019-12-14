import unittest
import re
import scraper
	
"""
this is a regression test. 
changing functionality will cause things here to break. 
"""

class MyTestCase(unittest.TestCase):


    def test_scraper.url_is_valid(self):
        self.assertFalse(scraper.url_is_valid("github.com"))
        self.assertFalse(scraper.url_is_valid("http:/github.com"))
        self.assertTrue(scraper.url_is_valid("https://github.com"))
        self.assertFalse(scraper.url_is_valid("https:/github.com"))

