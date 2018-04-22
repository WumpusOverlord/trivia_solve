
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




def analyse_results(answers, results):
    answer_scores = {}
    word_scores = {}
    metadata = results.metadata
    items = metadata["items"]
    # items = results.metadata.items
    for answer in answers[0:3]:
        answer_scores[answer]=0
        answer = answer.lower()
        for item in items:
            snippet = item['snippet']
            if answer in snippet.lower():
                answer_scores[answer] = answer_scores[answer]+1
            seperate_words = answer.split()
            for word in seperate_words:
                word_scores[word]=0
                for item in items:
                    snippet = item['snippet']
                if word in snippet:
                    word_scores[word] = word_scores[word]+1
    print(answer_scores)
    return results, word_scores, answer_scores

def get_entity_occurence_count(question_entities, entity_occurences_dict):

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
def analyse_wikis(question_entities, answer_wikis):
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




def get_occurences_in_question_content(entities, q_content):
    entity_occurences = {}
    for entity in entities:
        entity_lower = entity.lower()
        entity_index = allindices(q_content.lower(), entity.lower(), listindex=[], offset=0)
        entity_occurences[entity_lower] = entity_index
    return entity_occurences




def get_occurences_in_wiki_content(entities, wiki_content):
    entity_occurences = {}
    for entity in entities:
        entity_lower = entity.lower()
        entity_index = allindices(wiki_content.lower(), entity.lower(), listindex=[], offset=0)
        entity_occurences[entity_lower] = entity_index

        for entity_index in entity_occurences[entity_lower]:
            if len(entity_occurences[entity_lower])<4:
                print('\t' + wiki_content.lower()[entity_index-10:(entity_index+len(entity))])
        # print(wiki_content.lower())

    return entity_occurences

#
#
# def get_occurences_in_wiki_links(word, wiki_links):


# gets content of wiki
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
            x=""
    return entity_wiki_titles


def allindices(string, sub, listindex=[], offset=0):
    i = string.find(sub, offset)
    while i >= 0:
        listindex.append(i)
        i = string.find(sub, i + 1)
    return listindex
