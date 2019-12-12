from bs4 import BeautifulSoup
from flask import jsonify
from requests_futures.sessions import FuturesSession
import requests
import sys
import os

num_workers = os.cpu_count() * 2
session = FuturesSession(max_workers=num_workers)


def checkProtocol(url):
    # Validate argument starts with http or https
    return url.startswith('http://') or url.startswith('https://')


def linkCheck(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        print ("going in!", file=sys.stderr)
        
        value = {}
        header_items = soup.find_all("div", class_="header__stats__item")
        value["app_name"] = app_name = soup.find_all("h1", itemprop="name", class_="header__title")[0].text
        value["download_count"] = download_count = header_items[0].find_all("span")[1].text
        value["version"] = version = header_items[1].find_all("span")[1].text
        foo = soup.find_all("tr", class_="app-info__row")
        for tr_app_info_row in foo:
            td = tr_app_info_row.find("td", string=lambda text: text is not None and "Release" in text)
            if td:
                value["release_date"] = release_date = tr_app_info_row.find_all()[1].text[:10]
        value["app_description"] = app_description = soup.find("p", itemprop="description").text
                
        print ("done!", file=sys.stderr)                
        
        jsonData = []
        urls = []
        futures = []
        for feature in value:
            # Append keypairs
            jsonData.append(
                {'code': feature, 'url': value[feature]})
        return jsonData
    except requests.ConnectionError:
        return jsonify({'error': 'unable to connect'})
    except requests.exceptions.MissingSchema:
        return jsonify({'error': 'missing http://'})
    except(Exception) as e:
        print(e, file=sys.stderr)
        return jsonify({'error': 'unknown'})


def validate_json(request_json):
    try:
        if request_json["url"]:
            return request_json["url"]
    except(Exception) as e:
        raise KeyError('url key not in json')
