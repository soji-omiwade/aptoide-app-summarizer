"""This script implements the APIs for a website to scrape aptoide content.

Problem Statement:
After submitting the [aptoide app] URL, the website returns a page displaying
the following information about the App:
App's name
App's version
Number of downloads
Release date
App's description

To solve this problem, this script uses the BeautifulSoup API to parse the
aptoide html content. Of course, the parsing can be done with little or no use
of the BeautifulSoup module. For extensibility though, I used APIs when
possible. The idea is that we shouldn't reinvent the wheel by doing
what an established library has succeeded in doing. This makes my code
much less in content, and hence less confusing, and hence extensible.

If the content of the site changes and hence breaks this script, then we
may just need to change how we call the BeautifulSoup APIs and a little bit of
this script too. This should be quick.

The script is highly functional and every function returns only one type. This
allows for easier debugging and test case development. See the following for
example: ./tests/test_scraper.py

Finally, corner and edge cases are handled, where the site content has changed
or the URL is not an aptoide app URL
"""
from bs4 import BeautifulSoup
from bs4.element import Tag
from flask import jsonify
import flask
import requests
from enum import Enum


AppFeature = Enum("AppFeature", "App-Name Version Number-of-Downloads\
    Release-Date Description")


def url_is_valid(url: str) -> bool:
    """Every URL to the script must be some app on the aptoide market."""
    return (url.startswith('http://') or url.startswith('https://'))\
        and url.rstrip("/").endswith("aptoide.com")


def get_description_value(soup: BeautifulSoup) -> str:
    """Get the description value in the html via its unique class."""
    description_contents = soup.\
        find(class_="view-app__description").\
        find("p", itemprop="description").contents
    return "".join(str(content) for content in description_contents)


def get_feature_value(detailed_info_popup: Tag, feature: AppFeature):
    """Get the desired text for the given feature, from the div class.

    Search *only* within the given div Tag for the given feature passed in
    for the desired text, which turns out to be the second td sibling

    As long as the information exists we can scrape for it. The method
    gracefully moves past any missing field, and will show no value there.
    Upstream clients of this script can raise Exceptions if any field is
    accordingly empty
    """
    def clean_text(text: str) -> str:
        """Strip, lower case and remove the semi-colon.

        This allows for comparison based on just the alphanumeric text.
        Example: "App Name: " becomes "app name"
        """
        return text.lower().strip().replace(":", "")

    feature = feature.name.lower().replace("-", " ")
    return detailed_info_popup\
        .find("td", string=lambda text: feature == clean_text(text))\
        .next_sibling.next_sibling.text


def get_content(url) -> (requests.models.Response, flask.wrappers.Response):
    """Get the aptoide app content for html parsing."""
    try:
        response = None
        if url_is_valid(url):
            response = requests.get(url)
            if response and response.status_code == 200:
                return response.content, None
        raise Exception("invalid response")
    except requests.ConnectionError:
        return None, jsonify({'error': 'unable to connect'})
    except(Exception):
        return None, jsonify({'error': 'unknown'})


def get_app_summary(url: str) -> (list, flask.wrappers.Response):
    """Get the app features requested and return the result as a list.

    Via the BeautifulSoup, the method (and downstream methods) rely on
    BeautifulSoup API find and next_sibling to retrieve the necessary text.
    The description feature has a unique class, so that is easy to grab.
    The remaining features are found within yet another unique class.
    """
    aptoide_content, json_error_response = get_content(url)
    if not aptoide_content:
        return [], json_error_response

    soup = BeautifulSoup(aptoide_content, 'html.parser')
    app_info = {}
    detailed_info_popup\
        = soup.find("div", class_="popup__content popup__content--app-info")
    if not detailed_info_popup:
        return [], jsonify({'error': 'detailed info pop-up box missing'})

    for feature in AppFeature:
        if feature != AppFeature.Description:
            app_info[feature] = get_feature_value(detailed_info_popup, feature)
    app_info[AppFeature.Description] = get_description_value(soup)
    json_data = []
    for feature in app_info:
        json_data.append({
            'feature': feature.name.replace("-", " "),
            'value': app_info[feature]
        })
    return json_data, None
