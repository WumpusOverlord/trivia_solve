import io
import os
import json
from google.cloud import vision
#
# with open('config.json') as json_data_file:
#     data = json.load(json_data_file)
#
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=data["GOOGLE_APPLICATION_CREDENTIALS"]


def detect_labels(path):
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    my_response = response.text_annotations[0].description
    question = my_response.split('?')[0]
    answers = my_response.split(question)[1]
    question = question + "?"
    question = question.replace('\n', ' ')
    answers = answers.lower()
    answers = answers[1:]
    if answers.startswith("\n"):
        answers = answers[1:]
    answers = answers.splitlines()
    answers = answers[0:3]
    question = question.lower()
    return question, answers
