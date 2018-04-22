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

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

img_name = data["img_name"]
save_path = data["img_save_path"]
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=data["GOOGLE_APPLICATION_CREDENTIALS"]


def wait_for_key_to_solve():
    while True:
        try:
            keyboard.wait('esc')
            print('Solving')
            solve_trivia()
        except KeyboardInterrupt:
            print('All done')
            wait_for_key_to_solve()

def get_google_results(question, answers):
    results = gcs.google_custom_search(question)
    results, word_scores, answer_scores = ar.analyse_results(answers, results)
    links = results.links
    print('scraping site')
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
    return question, answers


def get_question_entity_occurence(e_occurences, question_word_occurence):

    min_index = -1
    min_difference =9999
    question_entity = ""
    for entity, entity_occerence in e_occurences.items():
        try:
            difference = entity_occerence[0]-question_word_occurence
            if difference > 0:
                if difference < min_difference:
                    min_difference = difference
                    min_index = entity_occerence
                    question_entity = entity
        except:
            pass
    return question_entity

def get_answer_entity_types(question, answers, question_entities):
    e_occurences = ar.get_occurences_in_question_content(question_entities, question.lower())
    q_occurences = ar.get_occurences_in_question_content(["what","which", "who"], question.lower())
    q_occurences = list(q_occurences.values())
    q_occurences = [j for i in q_occurences for j in i]
    if len(q_occurences) >= 0:
       question_word_occurence =  q_occurences[0]
       entity_occurence = get_question_entity_occurence(e_occurences, question_word_occurence)

    return entity_occurence

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


p = inflect.engine()

import time

def solve_question_answers(question, answers):

    try:
        answers = convert_answers_to_lower(answers)
        get_google_results(question, answers)
    except:
        pass

    # try:

    qas = gnl.get_entities(question)

    question_entities = []
    for question_entity in qas:

        question_en_sing = p.singular_noun(question_entity, count=None)
        if question_en_sing != False:
            question_entities.append(question_en_sing)
        else:
            question_entities.append(question_entity)


    try:


        t0 = time.time()


        google_results = gcs.get_google_screen_scrapes(question_entities, answers)
        t1 = time.time()

        total = t1-t0
        print("TOTAL TIME: " + str(total))

        answer_entity = get_answer_entity_types(question, answers, qas)
        answer_en_sing = p.singular_noun(answer_entity, count=None)
        if answer_en_sing != False:
            answer_entity = answer_en_sing
        question_entities.remove(answer_entity)
        answer_wikis = wl.get_wikis_with_entity(answers, answer_entity)
        # except:
        #     answer_wikis = wl.get_wikis(answers)

        # question_entities_wikis = wl.get_wikis(question_entities)
        answers_wikis = answer_wikis[1]
        entity_occurences = ar.analyse_wikis(question_entities, answers_wikis)
        entity_occurence_count = ar.get_entity_occurence_count(question_entities, entity_occurences)
        # except:
        #     print('unknown wiki occs')
        # analyse the occurence of answer entities in question wikis
        answers = convert_answers_to_lower(answers)
    except:
        pass
    # get_google_results(question, answers)

def convert_answers_to_lower(answers):
    lower_answers = []
    for answer in answers:
        lower_answer = answer.lower()
        lower_answers.append(lower_answer)
    return lower_answers

def solve_trivia():
    try:
        question, answers = get_img_labels()
        # print(question + answers)
        solve_question_answers(question, answers)
    except:
        print('uh oh')

#
question = "What do Edward Norton and Christian Slater share?"
answers = ["Birthday", "Piano Teacher", "Aunt/Mother"]

#34
# question = "which of these celebrities has not published a cookbook?"
# answers = ["coolio", "lily alan", "Pippa middleton"]
solve_question_answers(question, answers)



#
# keyboard.wait('esc')
# wait_for_key_to_solve()
