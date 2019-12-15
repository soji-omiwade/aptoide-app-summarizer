import unittest
import re
import scraper
from bs4 import BeautifulSoup
from flask import jsonify
import requests
from enum import Enum 
import sys
	
class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_url_is_valid(self):
        self.assertFalse(scraper.url_is_valid("github.com"))
        self.assertFalse(scraper.url_is_valid("http:/github.com"))
        self.assertTrue(scraper.url_is_valid("https://github.com"))
        self.assertFalse(scraper.url_is_valid("https:/github.com"))

    def test_url_is_valid(url):
        pass
        
    def test_get_description_value(soup):
        pass
            
    def test_get_value_from_detailed_info(test, soup, feature):
        pass

    def test_get_aptoide_content(self, url):
        pass
    
    def test_extract_info(self, url):
        pass