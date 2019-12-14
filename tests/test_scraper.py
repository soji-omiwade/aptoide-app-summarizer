import unittest
import re
import scraper
	
"""
this is a regression test. 
changing functionality will cause things here to break. 
"""

class MyTestCase(unittest.TestCase):
    def test_checkProtocol(self):
        self.assertFalse(scraper.checkProtocol("github.com"))
        # assert checkProtocol("http:/github.com") == False
        # assert checkProtocol("https://github.com") == True
        # assert checkProtocol("https:/github.com") == False

