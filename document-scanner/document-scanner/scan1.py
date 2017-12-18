# USAGE
# python scan.py --image images/page.jpg 

# import the necessary packages
import argparse
import sys

import cv2
from skimage.filters import threshold_local

from pyimagesearch import imutils
from pyimagesearch.transform import four_point_transform

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(sys.argv[1])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
(image1, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

# show the contour (outline) of the piece of paper
# print "STEP 2: Find contours of paper"
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = threshold_local(warped, 3)
warped = warped.astype("uint8") * 255
warped = cv2.bitwise_not(warped)
image2 = cv2.GaussianBlur(warped, (5, 5), 0)
warped = cv2.addWeighted(warped, 1.5, image2, -0.5, 0, warped)

# save invoice
print cv2.imwrite("invoice1.jpg", warped)
print(sys.argv[1])
sys.stdout.flush()