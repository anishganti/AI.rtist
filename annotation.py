from functools import partial
import cv2
import numpy as np
from io import BytesIO

coords = []
drawing = False


def submit_annotation(img_height, img_width, file_name, value):
    # user chooses to submit
    if value == 100:
        # calculate center coordinates and bounding box dimensions
        x_center = ((coords[1][0] + coords[0][0]) / 2) / img_width
        y_center = ((coords[1][1] + coords[0][1]) / 2) / img_height
        width = (coords[1][0] - coords[0][0]) / img_width
        height = (coords[1][1] - coords[0][1]) / img_height

        # store annotation in YOLO txt file, the format should be
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
        coords = [(x, y)]

    if event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
        # user let go of button, finished drawing
        drawing = False

        # store final ending coordinates
        coords.append((x, y))

        # display final bounding box
        copy = img.copy()
        cv2.rectangle(copy, coords[0], coords[1], (0, 0, 255))
        cv2.imshow('image', copy)


def annotate_image(img_data, img_name):
    # read the image
    img_stream = BytesIO(img_data.content)
    img = cv2.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)

    if img is None:
        return
    # display the image
    cv2.imshow('image', img)

    # set mouse handler for the image to call draw_bounding_box() function
    cv2.setMouseCallback('image', draw_bounding_box, img)

    # grab image dimensions and name
    img_height, img_width, img_channels = img.shape

    # OpenCV doesn't have a button implementation
    # creating a trackbar to implement the reset/submit functionality
    # use functools.partial to pass in extra parameters to the callback function
    cv2.createTrackbar('submit', 'image', 0, 100, partial(submit_annotation, img_height, img_width, img_name))

    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    # close the window
    cv2.destroyAllWindows()
