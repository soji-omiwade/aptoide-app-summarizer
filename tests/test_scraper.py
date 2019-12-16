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
        self.aptoide_description_substring = "Keeping up with friends is faster"
        
    def test_url_is_valid(self):
        self.assertFalse(scraper.url_is_valid("github.com"))
        self.assertFalse(scraper.url_is_valid("http:/github.com"))
        self.assertTrue(scraper.url_is_valid("https://github.com"))
        self.assertFalse(scraper.url_is_valid("https:/github.com"))
        
    def test_get_description_value(self):
        with open("tests/facebook_contents.in", "rb") as f:
            self.aptoide_content = f.read()    
        soup = BeautifulSoup(self.aptoide_content, 'html.parser')
        self.assertTrue(self.aptoide_description_substring
            in scraper.get_description_value(soup))       
            
    def test_get_value_from_detailed_info(self):
        with open("tests/facebook_contents.in", "rb") as f:
            self.aptoide_content = f.read()    
        expected_popup_results\
        = ["Facebook", "1.0.10", "50M - 250M", "2019-12-11 19:12:35"]
        for expected, feature in zip(expected_popup_results, scraper.AppFeature):
            soup = BeautifulSoup(self.aptoide_content, 'html.parser')
            self.assertEqual(expected
                , scraper.get_value_from_detailed_info(soup, feature))
        
    def test_get_app_info_in_json_form_for_valid_url(self):
        url = "https://facebook.en.aptoide.com/"
        expected_popup_results\
        = ["Facebook", "1.0.10", "50M - 250M", "2019-12-11 19:12:35"]

        json_data = scraper.get_app_info_in_json_form(url)
        
        #first check the string is contained
        self.assertTrue(json_data[4]["feature"], scraper.AppFeature.Description.name)
        self.assertTrue(self.aptoide_description_substring in json_data[4]["value"])

        expected_json_data = []
        for feature, result in zip(scraper.AppFeature, expected_popup_results):
            expected_json_data.append({'feature': feature.name, 'value': result})
        
        #pop the description, since expected_json_data doesn't include items
        #and we already validated it correctly 
        json_data.pop()
        
        #now check on equality
        self.assertEqual(json_data, expected_json_data)
        
class ConnectionTestCase(unittest.TestCase):

    def test_get_aptoide_content(self):
        url = "https://facebook.en.aptoide.com/"
        aptoide_content, json_error_response = scraper.get_aptoide_content(url)
        self.assertIsNone(json_error_response)
        self.assertIsNotNone(aptoide_content)

    def test_get_aptoide_content(self):
        url = "https://facebook.en.aptoodde.com/"
        self.assertRaises(RuntimeError, scraper.get_aptoide_content, url)       
