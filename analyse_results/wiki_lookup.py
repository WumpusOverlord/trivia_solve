import wikipedia
from wikitables import import_tables
tables = import_tables('List of cities in Italy') #returns a list of WikiTable objects

#
# def wiki_search(query):
#
#     r = requests.get(API_URL, params=params, headers=headers)
#
#     raw_results = _wiki_request(search_params)


def wiki_lookup(answer):
    try:
        ny = wikipedia.page(answer)
    except:
        return ""
    return ny
# question = "Which of these is a common material used in 3D printers"
# wiki_lookup("3D printers")

# def get_wikis(answers):
#     answer_wikis = {}
#     for answer in answers:
#         answer_wiki = wiki_lookup(answer)
#         answer_wikis[answer] = answer_wiki
#
#     return answer_wikis



import asyncio
def get_wikis(question):
    answers = question.answers
    answers_with_entities = []
    for answer in answers:
        answers_with_entities.append(answer.answer_with_entity)
    queries = answers_with_entities
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(queries))
    data = loop.run_until_complete(future)
    return answers, data

#
# async def fetch_all(session, urls, loop):
#     results = await asyncio.gather(*[loop.create_task(fetch(session, url))
#                                      for url in urls])
#     return results
#




async def fetch_page(response, session):
    API_URL = 'http://en.wikipedia.org/w/api.php'
    pageid = response['query']['search'][0]['pageid']
    search_params = {
        'prop': 'info|pageprops',
        'inprop': 'url',
        'ppprop': 'disambiguation',
        'redirects': '',
        'pageids': pageid
    }

    USER_AGENT = 'wikipedia (https://github.com/goldsmith/Wikipedia/)'
    search_params['format'] = 'json'
    if not 'action' in search_params:
        search_params['action'] = 'query'
    headers = {
        'User-Agent': USER_AGENT
    }

    async with session.get(API_URL, params=search_params, headers=headers) as response:

        wiki_json = await response.json()
        # wikipediapage(pageid = wwiki-json['pageid'])
        return wiki_json



async def fetch(query, session):

    API_URL = 'http://en.wikipedia.org/w/api.php'

    search_params = {
        'list': 'search',
        'prop': 'extracts',
        'srprop': '',
        'srlimit': 1,
        'srsearch': query
    }

    USER_AGENT = 'wikipedia (https://github.com/goldsmith/Wikipedia/)'
    search_params['format'] = 'json'
    if not 'action' in search_params:
        search_params['action'] = 'query'
    headers = {
        'User-Agent': USER_AGENT
    }

    async with session.get(API_URL, params=search_params, headers=headers) as response:

        wiki_json = await response.json()
        # wikipediapage(pageid = wwiki-json['pageid'])
        return wiki_json

# def get_wiki_page(pageid):
#     query_params = {
#         'prop': 'info|pageprops',
#         'inprop': 'url',
#         'ppprop': 'disambiguation',
#         'redirects': '',
#         'pageids': 'pageid'
#     }
#
#     request = _wiki_request(query_params)
#
#     query = request['query']
#     pageid = list(query['pages'].keys())[0]
#     page = query['pages'][pageid]


import aiohttp
async def run(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        wiki_pages = []
        for response in responses:
            pageid = response['query']['search'][0]['pageid']
            try:
                ny = wikipedia.page(pageid=pageid)
                wiki_pages.append(ny)
            except:
                wiki_pages.append("")
    return wiki_pages



def get_wikis_with_entity(question):
    # answer_with_entities = []
# answers, entity

    for answer in question.answers:
        answer_with_entity = answer.lower + " " + question.answer_entity_type_singular
        answer.set_answer_with_entity(answer_with_entity)

    answer_wikis = get_wikis(question)
    return answer_wikis


def get_words_count_in_wiki(words, wiki):
    word_counts = {}
    for word in words:
        word_count = wiki.content.lower().count(word.lower())
        word_counts[word] = word_count
    return word_counts


def convert_entities(urls):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run_entity(urls))
    data = loop.run_until_complete(future)
    titles = {}
    i = 0
    for answer_wiki in data:
        try:
            title = answer_wiki['query']['search'][0]['title']
            print(title)
            titles[urls[i]] = title
        except:
            pass
        i=i+1
    return titles



async def run_entity(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

# answer_wikis = convert_entities(["cookbook"])
# print('done')
