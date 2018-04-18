import screen_scrape.screen_grab as sg
import google_api.vision_lookup as vl
import google_api.custom_search as cs
import analyse_results.analyse_results as ar
from pygame.locals import *
import pygame, sys

import keyboard

def wait_for_key_to_solve():

    while True:
        keyboard.wait('esc')
        print('BREAK')



def solve_trivia():
    save_path = '../data'
    img_name = "cropped_in_memory_to_disk.png"
    image_path = sg.screen_grab(save_path, img_name)
    question, answers = vl.detect_labels(image_path)
    answers = answers[0:3]
    results = cs.google_custom_search(question)
    results, word_scores, answer_scores = ar.analyse_results(answers, results)

    links = results.links
    print('scraping site')
    for link in results.links:
        website_text = cs.scrape_website(link)
        website_word_scores, website_answer_scores = ar.website_score(answers, website_text)
        for answer in answers:

            answer_scores[answer] = website_answer_scores[answer] + answer_scores[answer]
            for word in answer.split():
                word_scores[word] = website_word_scores[word] + word_scores[word]

        print(word_scores)
        print("-------------------")
        print(answer_scores)
    print('x')

# solve_trivia()

wait_for_key_to_solve()
