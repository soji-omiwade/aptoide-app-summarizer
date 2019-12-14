from bs4 import BeautifulSoup
from flask import jsonify
import requests
from enum import Enum 
import sys
AppFeature = Enum("AppFeature", 
"App-Name Version Number-of-Downloads Release-Date Description")

def url_is_valid(url):
    # Validate argument starts with http or https
    return url.startswith('http://') or url.startswith('https://')

def get_description_value(soup):
    return soup.\
        find(class_="view-app__description").\
        find("p", itemprop="description").text

    
def get_value_from_detailed_info(soup, feature):
    """ as long as the detailed information exists we can scrape
        the website for everything except the description. 
        description is not there, but the method gracefully moves past it
    """
        
    rows = soup.find("div", class_="popup__content popup__content--app-info")
    cleaned_query = feature.name.lower().replace("-"," ")
    cleaned_string = lambda text: text.lower().strip().replace(":", "")
    foo = lambda text: cleaned_query == cleaned_string(text)
    return rows.find("td", string = foo).next_sibling.next_sibling.text


def get_aptoide_content(url): 
    try:
        response = requests.get(url)
        if response and response.status_code == 200: 
            aptoide_content = response.content
        else: raise Exception("invalid response")
    except requests.ConnectionError as e:
        print("conn-err: ", e, file=sys.stderr)
        return None, jsonify({'error': 'unable to connect'})
    except(Exception) as e:
        print("except-err: ", e, file=sys.stderr)
        return None, jsonify({'error': 'unknown'})
    return aptoide_content, None
    
    
def extract_info(url):

    aptoide_content, json_error_response = get_aptoide_content(url)
    
    if not aptoide_content: 
        return json_error_response
        
    soup = BeautifulSoup(aptoide_content, 'html.parser')
    app_info = {}

    for feature in AppFeature:
        if feature != AppFeature.Description:
            app_info[feature] = get_value_from_detailed_info(soup, feature)
        
    app_info[AppFeature.Description] = get_description_value(soup)
                
    json_data = []
    for feature in app_info:
        json_data.append({'feature': feature.name, 'value': app_info[feature]})

    return json_data