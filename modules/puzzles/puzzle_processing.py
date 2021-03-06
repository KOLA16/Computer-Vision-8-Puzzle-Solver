"""
puzzle_processing.py

Defines functions responsible for detecting, processing a puzzle,
and extracting puzzle's cells.

"""

import numpy as np
import imutils
import cv2
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border


class PuzzleNotFoundError(Exception):
    """
    The exception that is raised when find_puzzle method
    fails to detect the puzzle contour
    """

    pass


def find_puzzle(frame):
    """
    Detects a puzzle contour on the video frame returns
    a top down bird's eye view of the puzzle
    """
    # convert the image to grayscale and blur it slightly
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)

    # apply adaptive thresholding and then invert the threshold map
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    thresh = cv2.bitwise_not(thresh)

    # find contours in the thresholded image and sort them by size in
    # descending order
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
                                cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # initialize a contour that corresponds to the puzzle outline
    puzzle_cnt = None

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)

        # ensure that the approximated contour is rectangular
        if len(approx) == 4:
            # compute the bounding box of the approximated contour and
            # use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)

            # compute whether or not the width and height, and
            # aspect ratio of the contour falls within appropriate bounds
            keepDims = w > 45 and h > 45
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            # ensure that the contour passes all our tests
            if keepDims and keepAspectRatio:
                puzzle_cnt = approx
                cv2.drawContours(frame, [puzzle_cnt], -1, (0, 255, 0), 2)
                break

    if puzzle_cnt is None:
        raise PuzzleNotFoundError()

    # obtain a top-down bird's eye view of the puzzle
    transformed = four_point_transform(gray, puzzle_cnt.reshape(4, 2))

    return transformed


def extract_digit(cell):
    """
    Extracts a digit contour from a single cell
    Returns a masked image of a digit
    It also returns a boolean to indicate if cell is empty or not
    """

    empty = True

    # apply automatic thresholding to the cell and then clear any
    # connected borders that touch the border of the cell
    thresh = cv2.threshold(cell, 0, 255, 
                                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)

    # find contours in the thresholded cell
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
                                cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # if no contours were found than this is an empty cell
    if len(cnts) == 0:
        return None, empty

    # otherwise, find the largest contour in the cell and create a
    # mask for the contour
    empty = False
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # apply the mask to the thresholded cell
    digit = cv2.bitwise_and(thresh, thresh, mask=mask)

    return digit, empty
