import numpy as np
import pyautogui
import cv2
import os
import json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# import matplotlib.pyplot as plt

def take_screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image


def crop_screenshot(save_path, img_name, img):
    x = data["airmore_crop_region"]
    crop_img = img[x[0]:x[1], x[2]:x[3], :]
    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # plt.imshow(crop_img)
    # plt.show()
    completeName = os.path.join(save_path, img_name)
    cv2.imwrite(completeName, crop_img)
    return completeName

def screen_grab(save_path, img_name):
    image = take_screenshot()
    completeName = crop_screenshot(save_path, img_name, image)
    return completeName

# screen_grab("x", "b")
