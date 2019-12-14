from bs4 import BeautifulSoup
from flask import jsonify
import requests
from enum import Enum 

AppFeature = Enum("AppFeature", 
    "App-Name Version Number-of-Downloads Release-Date Description")

def url_is_valid(url):
    # Validate argument starts with http or https
    return url.startswith('http://') or url.startswith('https://')

def add_description_key_value_info(soup, app_info):
    description_tag_with_breaks = soup.find(class_="view-app__description").\
        find("p", itemprop="description")
    app_info[AppFeature.Description] = description_tag_with_breaks.text
    
def add_available_key_value_info(soup, app_info):
    """ as long as the detailed information exists we can scrape
        the website for everything except the description. 
        description is not there, but the method gracefully moves past it
    """
        
    rows = soup.find("div", class_="popup__content popup__content--app-info")
    for feature in AppFeature:
        cleaned_query = feature.name.lower().replace("-"," ")
        cleaned_string = lambda text: text.lower().strip().replace(":", "")
        app_info[feature] = rows.find("td", string=lambda text: cleaned_query == cleaned_string(text)).next_sibling.next_sibling.text
    
    
def extract_info(url):

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        app_info = {}

        add_available_key_value_info(soup, app_info)
        add_description_key_value_info(soup, app_info)
                
        json_data = []
        for feature in app_info:
            json_data.append\
                ({'feature': feature.name, 'value': app_info[feature]})
        return json_data
    except requests.ConnectionError:
        return jsonify({'error': 'unable to connect'})
    except requests.exceptions.MissingSchema:
        return jsonify({'error': 'missing http://'})
    except(Exception) as e:
        raise e
        return jsonify({'error': 'unknown'})