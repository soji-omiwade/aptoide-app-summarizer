import unittest
import scraper
from bs4 import BeautifulSoup
from scraper import url_is_valid, AppFeature


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.aptoide_description_substring = "Keeping up with friends is fast"

    def test_url_is_valid(self):
        self.assertFalse(url_is_valid("github.com"))
        self.assertFalse(url_is_valid("http:/github.com"))
        self.assertFalse(url_is_valid("https://github.com"))
        self.assertFalse(url_is_valid("https:/github.com"))
        self.assertTrue(url_is_valid("https://facebook.en.aptoide.com/"))

    def test_get_description_value(self):
        with open("tests/facebook_contents.in", "rb") as f:
            self.aptoide_content = f.read()
        soup = BeautifulSoup(self.aptoide_content, 'html.parser')
        self.assertTrue(self.aptoide_description_substring
                        in scraper.get_description_value(soup))

    def test_get_detailed_info_value(self):
        with open("tests/facebook_contents.in", "rb") as f:
            self.aptoide_content = f.read()
        expected_results\
            = ["Facebook", "1.0.10", "50M - 250M", "2019-12-11 19:12:35"]
        for result, feature in zip(expected_results, AppFeature):
            soup = BeautifulSoup(self.aptoide_content, 'html.parser')
            self.assertEqual(result, scraper.get_feature_value(soup, feature))

    def test_get_app_summary_for_valid_url(self):
        url = "https://facebook.en.aptoide.com/"
        expected_results\
            = ["Facebook", "1.0.10", "50M - 250M", "2019-12-11 19:12:35"]

        json_data, _ = scraper.get_app_summary(url)

        # first check the string is contained
        self.assertTrue(json_data[4]["feature"], AppFeature.Description.name)
        self.assertTrue(
            self.aptoide_description_substring in json_data[4]["value"])

        expected_json = []
        for feature, result in zip(AppFeature, expected_results):
            expected_json.append({
                'feature': feature.name.replace("-", " "),
                'value': result
            })

        # pop the description, since expected_json doesn't include items
        # and we already validated it correctly
        json_data.pop()

        # now check on equality
        self.assertEqual(json_data, expected_json)


class ConnectionTestCase(unittest.TestCase):

    def test_get_aptoide_content(self):
        url = "https://facebook.en.aptoide.com/"
        aptoide_content, json_error_response = scraper.get_content(url)
        self.assertIsNone(json_error_response)
        self.assertIsNotNone(aptoide_content)

    def test_get_aptoide_content_via_bad_url(self):
        url = "https://facebook.en.aptoodde.com/"
        self.assertRaises(RuntimeError, scraper.get_content, url)
