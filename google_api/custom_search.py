
import search_google.api
import pandas as pd
import requests
from bs4 import BeautifulSoup

import numpy as np


# Define buildargs for cse api
buildargs = {
    'serviceName': 'customsearch',
    'version': 'v1',
    'developerKey': 'AIzaSyAdBj2ReANUUvy2HkfU9ao5tBNps5UmHKM'
}


def google_custom_search(question):
    cseargs = {
        'q': question,
        'cx': '002540799615767059181:rs9wevaoahs',
        'num': 10
    }
    print('scraping: ' + question)
    results = search_google.api.results(buildargs, cseargs)
    return results


def scrape_answers(brand_csv):
    brands_list = pd.read_csv(brand_csv, dtype=str, delimiter='\n')
    brand_dictionary = {}
    urls_array = []
    for brand in brands_list['Brands']:
        results = search_for_brand(brand)
        brand_dictionary[brand] = results.links
    return brand_dictionary


def scrape_website(url):
    text_array = []
    # ADD IN IF INTERNET CONNECTION IS DOWN
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for text in soup.find_all('p'):
        text_string = text.get_text()
        try:
            text_array.append(text_string)
        except:
            None
    text_array = " ".join(text_array)
    return text_array


def scrape_brand(brand_websites):
    website_content_array = []
    for url in brand_websites:
        website_text_array = scrape_website(url)
        url_content = [url, website_text_array]
        website_content_array.append(url_content)
    return website_content_array

def get_website_contents():
    brand_csv = '../data/Archive/Brands_test.csv'
    brand_dictionary = scrape_brands(brand_csv)
    print(brand_dictionary)
    for brand in brand_dictionary:
        print(brand)
        brand_websites = (brand_dictionary[brand])
        website_content_array = scrape_brand(brand_websites)
        brand_dictionary[brand]=website_content_array

