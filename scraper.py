from bs4 import BeautifulSoup
from flask import jsonify
import requests
from enum import Enum
AppFeature = Enum(
                "AppFeature", "App-Name Version Number-of-Downloads\
                Release-Date Description")


def url_is_valid(url):
    """Validate argument starts with http or https"""

    return (url.startswith('http://') or url.startswith('https://'))\
        and url.rstrip("/").endswith("aptoide.com")


def get_description_value(soup):
    description_contents = soup.\
        find(class_="view-app__description").\
        find("p", itemprop="description").contents
    return "".join(str(content) for content in description_contents)


def get_detailed_info_value(detailed_info_popup, feature):
    """get_detailed_info_value

    as long as the detailed information exists we can scrape
    the website for everything except the description.
    description is not there, but the method gracefully moves past it.
    the lower is necessary  because of number of downloads!
    and a good idea in general
    """
    def clean_info_field(text):
        return text.lower().strip().replace(":", "")

    feature = feature.name.lower().replace("-", " ")
    return detailed_info_popup\
        .find("td", string=lambda text: feature == clean_info_field(text))\
        .next_sibling.next_sibling.text


def get_aptoide_content(url):
    try:
        response = None
        if url_is_valid(url):
            response = requests.get(url)
        if response and response.status_code == 200:
            aptoide_content = response.content
        else:
            raise Exception("invalid response")
    except requests.ConnectionError:
        return None, jsonify({'error': 'unable to connect'})
    except(Exception):
        return None, jsonify({'error': 'unknown'})
    return aptoide_content, None


def get_app_info_in_json_form(url):

    aptoide_content, json_error_response = get_aptoide_content(url)

    if not aptoide_content:
        return json_error_response

    soup = BeautifulSoup(aptoide_content, 'html.parser')
    app_info = {}

    detailed_info_popup\
        = soup.find("div", class_="popup__content popup__content--app-info")
    if detailed_info_popup:
        for feature in AppFeature:
            if feature != AppFeature.Description:
                app_info[feature]\
                    = get_detailed_info_value(detailed_info_popup, feature)

    app_info[AppFeature.Description] = get_description_value(soup)

    json_data = []
    for feature in app_info:
        json_data.append({'feature': feature.name, 'value': app_info[feature]})

    return json_data
