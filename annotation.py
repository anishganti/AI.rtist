import cv2
import numpy as np
from io import BytesIO

coords = []
drawing = False


def resize_with_padding(img):
    # default size for YOLOv5 is 640x640
    # scale the image so that the larger dimension is 640
    height, width, channels = img.shape
    scale = 640 / max(height, width)
    img = cv2.resize(img, (int(scale * height), int(scale * width)))

    # add padding to make the image 640x640
    # separate each side to take care of rounding issues
    height, width, channels = img.shape
    delta_w = 640 - width
    delta_h = 640 - height
    top, bottom = int(delta_h / 2), delta_h - int(delta_h / 2)
    left, right = int(delta_w / 2), delta_w - int(delta_w / 2)
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    print(img.shape)

    return img


def submit_annotation(img_height, img_width, file_name):
    # calculate center coordinates and bounding box dimensions for image
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

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        # user started drawing box
        # store the initial starting coordinates
        drawing = True
        coords = [(x, y)]

    elif event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
        # user let go of button, finished drawing
        drawing = False

        # store final ending coordinates
        coords.append((x, y))

        # display final bounding box
        copy = img.copy()
        cv2.rectangle(copy, coords[0], coords[1], (0, 0, 255))
        cv2.imshow('image', copy)


def annotate_image(img_data, img_name):
    global coords
    # read the image
    img_stream = BytesIO(img_data.content)
    img = cv2.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)

    if img is None:
        return True

    # resize the image to fit YOLOv5 model input format
    img = resize_with_padding(img)

    # display the image
    cv2.imshow('image', img)

    # set mouse handler for the image to call draw_bounding_box() function
    cv2.setMouseCallback('image', draw_bounding_box, img)

    # grab image dimensions and name
    img_height, img_width, img_channels = img.shape

    # handle user keystroke actions
    next = False
    while next is False:
        # get value of key user pressed
        key = cv2.waitKey(0)
        if key == 27:
            # user pressed 'esc', exit the program
            return False

        elif key == 3 or key == 13:
            # user pressed right arrow or enter, go to next submission
            next = True

        elif key == 2 or key == 127:
            # user pressed left arrow or backspace, clear the bounding box
            print('hi')
            coords = []
            cv2.imshow('image', img.copy())

    # submit the annotation only if there exists a bounding box
    if len(coords) != 0:
        submit_annotation(img_height, img_width, img_name)

    # close the window
    cv2.destroyAllWindows()
    return True
