
import wikipedia

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

def get_wikis(answers):
    answer_wikis = {}
    for answer in answers:
        answer_wiki = wiki_lookup(answer)
        answer_wikis[answer] = answer_wiki

    return answer_wikis



import asyncio
def get_wikis(answers):
    str = ""
    # question = " ".join(question_entities)
    # urls = get_wiki_urls(question, answers)
    # urls = get_wikis(answers)
    queries = answers

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(queries))
    data = loop.run_until_complete(future)
    # loop.close()
    # for x in range(0,len(answers)):
    #     print(answers[x] + " " + data[x])
    return answers, data


async def fetch_all(session, urls, loop):
    results = await asyncio.gather(*[loop.create_task(fetch(session, url))
                                     for url in urls])
    return results





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



def get_wikis_with_entity(answers, entity):
    answer_wikis = []
    answer_with_entities = []
    for answer in answers:
        answer_with_entity = answer + " " + entity

        answer_with_entities.append(answer_with_entity)
        #
        # answer_wikis[answer] = answer_wiki

    answer_wikis = get_wikis(answer_with_entities)
    return answer_wikis


def get_words_count_in_wiki(words, wiki):

    word_counts = {}
    for word in words:
        word_count = wiki.content.lower().count(word.lower())
        word_counts[word] = word_count

    return word_counts
