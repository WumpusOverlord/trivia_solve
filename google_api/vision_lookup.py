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
    # print('x')
    # for text in texts:
    #     print('\n"{}"'.format(text.description))
    #     # text_parsed = text_parsed + text.description
    #
    #     text_parsed = text_parsed + '\n"{}"'.format(text.description)
    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                  for vertex in text.bounding_poly.vertices])
    #
    #     print('bounds: {}'.format(','.join(vertices)))

    # labels = response.label_annotations
    # print('Labels:')
    #
    # for label in labels:
    #     print(label.description)
    #     print(label.score)
    #     descriptions.append(label.description)
    #     scores.append(label.score)

    return question, answers

#
# question, answers = detect_labels("/home/jeffh/Documents/Projects/trivia_solver/trivia_solve/data/cropped_in_memory_to_disk.png")
# #
# print(response)
