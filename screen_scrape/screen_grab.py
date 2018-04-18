
# import the necessary packages
import numpy as np
import pyautogui
import imutils
import cv2
import os
import matplotlib.pyplot as plt



save_path = '../data'
img_name = "cropped_in_memory_to_disk.png"

# take a screenshot of the screen and store it in memory, then
# convert the PIL/Pillow image to an OpenCV compatible NumPy array
# and finally write the image to disk
def take_screenshot(save_path, img_name):
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)



    return image

# take_screenshot(save_path, img_name)


def crop_screenshot(save_path, img_name, img):
    # img = cv2.imread("/Users/Hugo/Documents/Projects/trivia_solve/data/screenshot_test.png")



    crop_img = img[500:1200, 930:1580, :]

    # crop_img = img[y:y + h, x:x + w]
    completeName = os.path.join(save_path, img_name)
    cv2.imwrite(completeName, crop_img)

    plt.imshow(crop_img)
    plt.show()
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)



def screen_grab():
    image = take_screenshot(save_path, img_name)
    crop_screenshot(save_path, img_name, image)


screen_grab()