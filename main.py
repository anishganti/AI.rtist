from functools import partial
from io import BytesIO

import numpy as np
from cv2 import cv2
import requests
from PIL import Image

coords = []
drawing = False
def submit_annotation(img_height, img_width, file_name, value):
    # user chooses to submit
    if value == 100:
        print('submit')

        # calculate center coordinates and bounding box dimensions
        x_center = ((coords[1][0] + coords[0][0])/2)/img_width
        y_center = ((coords[1][1] + coords[0][1])/2)/img_height
        width = (coords[1][0] - coords[0][0])/img_width
        height = (coords[1][1] - coords[0][1])/img_height

        # storing annotation in YOLO txt file, the format should be
        # <object-class> <x-center> <y-center> <width> <height>
        file = open(file_name, 'w+')
        file.write(str(0) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(width) + ' ' + str(height) + "\n")
        file.close()
def draw_bounding_box(event, x, y, flags, img):
    global coords, drawing

    # user has clicked the button
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        # user started drawing box
        # store the initial starting coordinates
        drawing = True
        coords = [(x,y)]

    if event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
        # user let go of button, finished drawing
        drawing = False

        # store final ending coordinates
        coords.append((x, y))

        # display final bounding box
        copy = img.copy()
        cv2.rectangle(copy, coords[0], coords[1], (0,0,255))
        cv2.imshow('image', copy)

def annotate_image(file_name):
    # read the image
    img = cv2.imread(file_name)

    # display the image
    cv2.imshow('image', img)

    # set mouse handler for the image to call draw_bounding_box() function
    cv2.setMouseCallback('image', draw_bounding_box, img)

    # grab image dimensions and name
    img_height, img_width, img_channels = img.shape
    img_name = file_name.split('/')[-1].split('.')[0]

    # OpenCV doesn't have a button implementation
    # creating a trackbar to implement the reset/submit functionality
    # use functools.partial to pass in extra parameters to the callback function
    cv2.createTrackbar('submit', 'image', 0, 100, partial(submit_annotation, img_height, img_width, img_name))

    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    # close the window
    cv2.destroyAllWindows()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #parse args

    #prompt user if they are sure they want to scrape for entered search phrase

    #if entere Y
    #annotate_image('/Users/anishganti/outfit inspo/image.jpg')
    img_data = requests.get('https://mylifeintheocean.files.wordpress.com/2012/11/tropical-ocean-wallpaper-1920x12003.jpg')
    img_data.raise_for_status()
    img_stream = BytesIO(img_data.content)
    img = cv2.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)
    cv2.imshow('img',img)
    cv2.waitKey(0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def scrape_data():

    search_term = 'canadian rockies'

    image_results = search_images(search_term)

    process_images(image_results)


def search_images(search_term):
    # code mostly pulled from Bing documentation

    # create and initialize the application
    subscription_key = 'Enter your key here'
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"

    # add your subscription key to the Ocp-Apim-Subscription-Key header
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    # create and send a search request
    params = {"q": search_term, "license": "public", "imageType": "photo"}

    # send search query to Bing Image Search API
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    img_urls = [img["contentUrl"] for img in search_results["value"]]

    # view the results
    #f, axes = plt.subplots(4, 4)
    for i in range(4):
        for j in range(4):
            img_data = requests.get(img_urls[i+4*j])
            img_data.raise_for_status()
            img = BytesIO(img_data.content)
            axes[i][j].imshow(image)
            axes[i][j].axis("off")
    plt.show()

def process_images(image_results):
    for image in image_results:
        annotate_image(image)