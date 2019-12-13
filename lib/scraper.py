from bs4 import BeautifulSoup
from flask import jsonify
import requests
from enum import Enum 

AppFeature = Enum("AppFeature", 
    "Name Version Number-of-Downloads Release-Date Description")


def add_description_key_value_info(soup, app_info):
    description_tag_with_breaks = soup.find(class_="view-app__description").\
        find("p", itemprop="description")
    for br in description_tag_with_breaks.find_all("br"):
        br.replace_with("\n")
    app_info[AppFeature.description] = description_tag_with_breaks.text

def add_available_key_value_info(soup, app_info):
    """ as long as the detailed information exists we can scrape
        the website for everything except the description
        
        the two lines below get the necessary information
        #description is not there, but the method gracefully moves past it
    """
    for feature in AppFeature:
        for tr_app_info_row in soup.find_all("tr", class_="app-info__row"):
            td_list = tr_app_info_row.find_all("td")
            if td_list and feature.name.lower().replace("-"," ") \
                    == td_list[0].text.lower():
                app_info[feature] = td_list[1].text


def extract_info(url):


    try:
        response = requests.get(url)
        content = clear_br_
        soup = BeautifulSoup(response.content, 'html.parser')
        app_info = {}

        add_description_key_value_info(soup, app_info)
        add_available_key_value_info(soup, app_info)
                
                
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
        return jsonify({'error': 'unknown'})