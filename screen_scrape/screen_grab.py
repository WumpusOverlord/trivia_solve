import numpy as np
import pyautogui
import cv2
import os

def take_screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image

def crop_screenshot(save_path, img_name, img):
    crop_img = img[550:1100, 150:710, :]
    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    completeName = os.path.join(save_path, img_name)
    cv2.imwrite(completeName, crop_img)
    return completeName

def screen_grab(save_path, img_name):
    image = take_screenshot()
    completeName = crop_screenshot(save_path, img_name, image)
    return completeName
