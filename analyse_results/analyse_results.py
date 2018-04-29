
def website_score(answers, website_text):
    answer_scores = {}
    word_scores = {}

    for answer in answers[0:3]:
        answer_scores[answer]=0
        answer = answer.lower()

        if answer in website_text.lower():
            answer_scores[answer] = answer_scores[answer]+1
        seperate_words = answer.split()
        for word in seperate_words:
            word_scores[word]=0
            if word in website_text.lower():
                word_scores[word] = word_scores[word]+1

    return word_scores, answer_scores

import pandas as pd
def analyse_resultsv2(question, search_term):
    results = question.google_results[search_term]
    items = results.metadata["items"]
    df = pd.DataFrame(data=items)
    # pd..items[][]

    y_vals = {}
    # for row in df:
    for answer in question.answers[0:3]:
        m = df[['snippet', 'title', str('pagemap')]]
        # m_vals = m.values

        # df["count"] = df["emails"].map(count_emails)


        y = m.applymap(lambda x: str.count(str(x), answer.lower))
        # print('sdf')
        y_vals[answer.lower] = y
        # y_vals.append(y)
        ans_string = sum(y_vals[answer.lower].values)
        print(answer.lower + "-  " + str(sum(ans_string)))
    return 'x'

# at = re.compile(r"@", re.I)
def count_emails(string):
    count = 0
    for i in at.finditer(string):
        count += 1
    return count

def analyse_results(question, search_term):
    results = question.google_results[search_term]
    answers = question.answers
    answer_scores = {}
    word_scores = {}
    metadata = results.metadata
    items = metadata["items"]
    for answer in answers[0:3]:

        answer.search_scores[search_term]=0
        for item in items:
            snippet = item['snippet']
            if answer.lower in snippet.lower():
                answer.search_scores[search_term] = answer.search_scores[search_term]+1

    for answer in answers[0:3]:
        word_scores = {}
        answer.set_word_scores(search_term, items)
    print(answer_scores)
    return results, word_scores, answer_scores

def get_entity_occurence_count(question, entity_occurences_dict):
    question_entities = question.convertedEntities
    print('\t')
    print(question_entities)
    for key, value in entity_occurences_dict.items():
        # print('\n')
        # if len(value.items())
        print(key, end = ' ')
        for entity, occs in value.items():
            print(str(len(occs)) + ",", end = ' ')
        print('\n')

    print('done!')

#analyse the occurence of question entities in the answer wikis
def analyse_wikis(question, answer_wikis):
    question_entities = question.convertedEntities
    # question_entities = get_wiki_titles(question_entities_wikis)
    question_entity_occurences = {}
    for answer_wiki in answer_wikis:
        try:
            answer_name = answer_wiki.title
            print(answer_name, end = "")
            question_entity_occurences[answer_name] = get_occurences_in_wiki_content(question_entities, answer_wiki.content)
        except:
            pass
    # occurence_text = answer_wiki.content
    return question_entity_occurences


# RETURNS THE LOCATIONS OF EACH ENTITY IN THE QUESTION






#
# def get_occurences_in_question_content(entities, q_content):
#     entity_occurences = {}
#     for entity in entities:
#         entity_lower = entity.lower()
#         entity_index = allindices(q_content.lower(), entity.lower(), listindex=[], offset=0)
#         entity_occurences[entity_lower] = entity_index
#     return entity_occurences

def get_occurences_in_wiki_content(entities, wiki_content):
    entity_occurences = {}
    for entity in entities:
        entity_lower = entity.lower()
        entity_index = allindices(wiki_content.lower(), entity.lower(), listindex=[], offset=0)
        entity_occurences[entity_lower] = entity_index

        for entity_index in entity_occurences[entity_lower]:
            if len(entity_occurences[entity_lower])<4:
                print('\t' + wiki_content.lower()[entity_index-10:(entity_index+len(entity))])
    return entity_occurences


def get_wiki_content(wiki):
    return wiki['content'].lower()

# Gets titles of wikis
def get_wiki_titles(question_entities_wikis):
    # NEED TO SAVE TO DICT
    entity_wiki_titles = []
    for key, value in question_entities_wikis.items():
        try:
            entity_wiki_title = value.original_title
            entity_wiki_titles.append(entity_wiki_title)
        except:
            pass
    return entity_wiki_titles

def allindices(string, sub, listindex=[], offset=0):
    i = string.find(sub, offset)
    while i >= 0:
        listindex.append(i)
        i = string.find(sub, i + 1)
    return listindex
