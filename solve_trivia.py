import keyboard
import screen_scrape.screen_grab as screen_grab
import os
import google_api.vision_lookup as gvl
import google_api.custom_search as gcs
import inflect
import analyse_results.analyse_results as ar
from analyse_results import google_natural_language as gnl
from analyse_results import wiki_lookup as wl
import json
import question as q
import time
import inflect
p = inflect.engine()


with open('config.json') as json_data_file:
    data = json.load(json_data_file)

img_name = data["img_name"]
save_path = data["img_save_path"]
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = data["GOOGLE_APPLICATION_CREDENTIALS"]


def wait_for_key_to_solve():
    while True:
        try:
            keyboard.wait('esc')
            print('Solving')
            solve_trivia()
        except KeyboardInterrupt:
            print('All done')
            wait_for_key_to_solve()


def analyse_google_results(question, search_terms):


    # for each result

    x = ar.analyse_resultsv2(question, search_terms)
    # results, word_scores, answer_scores = ar.analyse_resultsv2(question, search_terms)

    # results, word_scores, answer_scores = ar.analyse_results2(question, search_terms)
    # links = results.links
    print('scraping site')


def get_google_results(question):
    answers = question.answers

    # question.googleResults[question.text] = results
    results = gcs.google_custom_search(question.text)
    question.google_results[question.text] = results
    # return question.text
    #

    # for link in links:
    #     try:
    #         website_text = gcs.scrape_website(link)
    #         website_word_scores, website_answer_scores = ar.website_score(answers, website_text)
    #         for answer in answers:
    #             answer = answer.lower()
    #             answer_scores[answer] = website_answer_scores[answer] + answer_scores[answer]
    #             for word in answer.split():
    #                 word_scores[word] = website_word_scores[word] + word_scores[word]
    #
    #         print(word_scores)
    #         print("-------------------")
    #         print(answer_scores)
    #     except:
    #         pass


def get_img_labels():
    image_path = screen_grab.screen_grab(save_path, img_name)
    question, answers = gvl.detect_labels(image_path)
    question = q.Question(question)
    question.set_answers(answers)
    return question, answers


def get_question_entity_occurence(e_occurences, question_word_occurence):
    min_index = -1
    min_difference = 9999
    question_entity = ""
    for entity, entity_occerence in e_occurences.items():
        try:
            difference = entity_occerence[0] - question_word_occurence
            if difference > 0:
                if difference < min_difference:
                    min_difference = difference
                    min_index = entity_occerence
                    question_entity = entity
        except:
            pass
    return question_entity


def get_answer_entity_types(question, answers):



    answer_entity_type = question.get_answers_entity_type()

    # e_occurences = ar.get_occurences_in_question_content(question.convertedEntities, question.text.lower())
    # q_occurences = ar.get_occurences_in_question_content(["what", "which", "who"], question.text.lower())
    # q_occurences = list(q_occurences.values())
    # q_occurences = [j for i in q_occurences for j in i]
    # if len(q_occurences) >= 0:
    #     question_word_occurence = q_occurences[0]
    #     entity_occurence = get_question_entity_occurence(e_occurences, question_word_occurence)
    # question.set_entity(entity_occurence)
    # return entity_occurence

    #
    #
    # tokens = gnl.get_tokens()
    #
    # for token in tokens:
    #     token_content = token["content"]
    #     if token_content.lower().contains("which"):
    #
    # for each entity
    #
    #     entity_splits = split entity
    #     for e in entity_splits:
    #         if entity is two words get each one
    #         see which has the head_token_index == index["which"/"what"]


#
# def if_question_contains_most():
#




# import times


def clean_entities(question):
    qas = question.originalEntities
    converted_entities = wl.convert_entities(qas)
    question_entities = []
    for original_entity in qas:
        if original_entity not in converted_entities:
            converted_entity = original_entity
        else:
            converted_entity = converted_entities[original_entity]
        question_en_sing = p.singular_noun(converted_entity, count=None)
        if question_en_sing != False:
            question_entities.append(question_en_sing)
        else:
            question_entities.append(converted_entity)

    return question_entities

def build_question_search_terms(question):
    # search_term1 = answer +
    # search_terms
    for entity in question.convertedEntities:
        if entity.lower() != question.answer_entity_type_singular:
            for answer in question.answers:
                search_term = answer.text + " " + str(entity)
                answer.search_terms.append(search_term)

    if 'not' in question.text:
        question_part = question.text.split('not')[1]
        for answer in question.answers:
            search_term = answer.text + " " + str(question_part)
            answer.search_terms.append(search_term)

    # Should search for just the celeb name as well
    print('d')






def solve_question_answers(question):
    # try:
    convert_answers_to_lower(question)
    search_terms = get_google_results(question)
    analyse_google_results(question, search_terms=question.text)
    question.originalEntities = gnl.get_entities(question)
    question.convertedEntities = clean_entities(question)


    question.get_answers_entity_type()
    build_question_search_terms(question)
    t0 = time.time()


    google_results = gcs.get_google_screen_scrapes(question)
    t1 = time.time()
    total = t1 - t0
    print("TOTAL TIME: " + str(total))

    answer_wikis = wl.get_wikis_with_entity(question)
    answers_wikis = answer_wikis[1]
    entity_occurences = ar.analyse_wikis(question, answers_wikis)
    entity_occurence_count = ar.get_entity_occurence_count(question, entity_occurences)
    # answers = convert_answers_to_lower(question)
    # except:
    #     pass
    # get_google_results(question, answers)


def convert_answers_to_lower(question):

    answers = question.answers
    lower_answers = []
    for answer in answers:
        answer.lower = answer.text.lower()



def solve_trivia():
    try:
        question, answers = get_img_labels()
        question = q.Question(question)
        question.set_answers(answers)
        # print(question + answers)
        solve_question_answers(question)
    except:
        print('uh oh')


# #
question = q.Question("What do Edward Norton and Christian Slater share?")
answers = ["Birthday", "Piano Teacher", "Aunt/Mother"]

# 34

# question = q.Question("which of these celebrities has not published a cookbook")
# answers = ["Coolio", "Lily Alan", "Pippa Middleton"]


# question.set_answers(answers)
#
# solve_question_answers(question)

#
keyboard.wait('esc')
wait_for_key_to_solve()
