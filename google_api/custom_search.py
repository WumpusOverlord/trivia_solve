import search_google.api
import aiohttp
import asyncio
import json
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import question as q

with open('./config.json') as json_data_file:
    data = json.load(json_data_file)

buildargs = data["buildargs"]

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def google_custom_search(question):
    cseargs = {
        'q': question,
        'cx': data["cx"],
        'num': 10
    }
    print('scraping: ' + question)
    results = search_google.api.results(buildargs, cseargs)
    return results


def get_google_urls(question_text, answers):

    google_urls = []
    for answer in answers:
        words = question_text + " " + answer.lower
        assert isinstance(words, str), 'Search term must be a string'
        assert isinstance(1, int), 'Number of results must be an integer'
        escaped_search_term = words.replace(' ', '+')
        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, 1, 'en')
        google_urls.append(google_url)
    #     TO-DO: APPEND URL TO ANSWER
    return google_urls

def get_google_screen_scrapes(question):

    question_entities = question.convertedEntities
    questionText = " ".join(question_entities)
    question.googleSearchTerm = questionText
    google_urls = get_google_urls(questionText, question.answers)
    urls = google_urls
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    data = loop.run_until_complete(future)
    return data
    # loop.close()
    # for x in range(0,len(question.answers)):
    #     question.answers.append(q.Answer(question.answers[x]))
    #     print(question.answers[x] + " " + data[x])



async def fetch(url, session):
    async with session.get(url, headers=USER_AGENT) as response:
        response = await response.text()
        soup = BeautifulSoup(response, "lxml")
        result_count = soup.find('div',{'id':'resultStats'}).text
        return result_count


async def run(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
    return responses

async def fetch_all(session, urls, loop):
    results = await asyncio.gather(*[loop.create_task(fetch(session, url))
                                     for url in urls])
    return results



async def fetch(url, session):
    async with session.get(url, headers=USER_AGENT) as response:
        response = await response.text()
        soup = BeautifulSoup(response, "lxml")
        result_count = soup.find('div',{'id':'resultStats'}).text
        print(result_count)
        return response, result_count


async def run(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
    return responses

async def fetch_all(session, urls, loop):
    results = await asyncio.gather(*[loop.create_task(fetch(session, url))
                                     for url in urls])
    return results

async def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text

def scrape_website(url):
    text_array = []
    # ADD IN IF INTERNET CONNECTION IS DOWN
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "lxml")
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

