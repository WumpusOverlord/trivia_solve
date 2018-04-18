
# import the necessary packages
import numpy as np
import pyautogui
# import imutils
import cv2
import os
# import matplotlib.pyplot as plt


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

