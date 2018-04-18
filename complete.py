
from pygame.locals import *
import pygame, sys

import keyboard

import pygame, sys
from pygame.locals import *
# import the necessary packages
import numpy as np
import pyautogui
# import imutils
import cv2
import os
# import matplotlib.pyplot as plt



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

import argparse
import io
import os

from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/jeffh/Documents/Projects/Mortgages_Hackathon/mortgages_hackathon/data/my-key.json"


def detect_labels(path):
    descriptions = []
    scores = []
    """Detects labels in the file."""
    # vision.ImageAnnotatorClient.Credentials()
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # response = client.label_detection(image=image)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    text_parsed=""
    # text_parsed_2=""
    my_response = response.text_annotations[0].description
    question = my_response.split('?')[0]
    answers = my_response.split(question)[1]
    question = question + "?"
    question = question.replace('\n', ' ')
    answers = answers.lower()
    answers = answers[1:]
    aString = "hello world"
    if answers.startswith("\n"):
        answers = answers[1:]
    answers = answers.splitlines()
    return question, answers



def google_custom_search(question):
    cseargs = {
        'q': question,
        'cx': '002540799615767059181:rs9wevaoahs',
        'num': 10
    }
    print('scraping: ' + question)
    results = search_google.api.results(buildargs, cseargs)
    return results


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


def take_screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image

# take_screenshot(save_path, img_name)


def crop_screenshot(save_path, img_name, img):
    # img = cv2.imread("/Users/Hugo/Documents/Projects/trivia_solve/data/screenshot_test.png")



    crop_img = img[550:1100, 150:710, :]

    # crop_img = img[y:y + h, x:x + w]
    completeName = os.path.join(save_path, img_name)
    cv2.imwrite(completeName, crop_img)
    return completeName
    # plt.imshow(crop_img)
    # plt.show()
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)

def screen_grab(save_path, img_name):
    image = take_screenshot()
    completeName = crop_screenshot(save_path, img_name, image)
    return completeName



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



def wait_for_key_to_solve():

    # pygame.init()
    # pygame.display.set_mode((100,100))

    x=0
    while keyboard.is_pressed('esc') == False:
        # if x ==0:
        solve_trivia()
            # x=x+1
            # break

    # wait_for_key_to_solve()
    #
    # while True:
    #     try:
    #         solve_trivia()
    #     except:
    #         print('')
    #     for event in pygame.event.get():
    #         if event.type == QUIT: sys.exit()
    #         if event.type == KEYDOWN and event.dict['key'] == 50:
    #             wait_for_key_to_solve()
    #             break
    #
    #     pygame.event.pump()
    #     break

    # while True:
    #     solve_trivia()
    #     keyboard.wait('esc')
    #
    #
    # while 1:
    #     print x
    # if input() == 1:
    #     break
    #
    # wait_for_key_to_solve()
    #
    # if keyboard.press = 'esc':
    #
    # x=1
    # while x=1:
    #
    #     while True:
    #         keyboard.wait('esc')
    #
    #         solve_trivia()
    #



def solve_trivia():
    print('solving trivia')
    save_path = '/home/jeffh/Documents/Projects/trivia_solver/trivia_solve/data/'
    img_name = "cropped_in_memory_to_disk.png"
    image_path = screen_grab(save_path, img_name)
    question, answers = detect_labels(image_path)
    answers = answers[0:3]
    results = google_custom_search(question)
    results, word_scores, answer_scores = analyse_results(answers, results)

    links = results.links
    print('scraping site')
    for link in results.links:
        website_text = scrape_website(link)
        website_word_scores, website_answer_scores = website_score(answers, website_text)
        for answer in answers:

            answer_scores[answer] = website_answer_scores[answer] + answer_scores[answer]
            for word in answer.split():
                word_scores[word] = website_word_scores[word] + word_scores[word]

        print(word_scores)
        print("-------------------")
        print(answer_scores)
    print('x')

# solve_trivia()
# keyboard.wait('esc')
# for x in range(0,30):
wait_for_key_to_solve()
