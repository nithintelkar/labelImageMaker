import cv2
import numpy as np
import glob
import os

refPt = []
image = np.array([np.char])
path = '/home/ubuntu/PoC/*'


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("inputImage", image)


def main():
    files = sorted(glob.glob(path))
    global image
    # load images in directory
    for file in files:
        print (file)
        inputImg = cv2.imread(file)
        clone = inputImg.copy()
        binaryImg = np.zeros((inputImg.shape[0], inputImg.shape[1]))
        image = inputImg
        cv2.namedWindow("inputImage")
        cv2.setMouseCallback("inputImage", click_and_crop)

        # keep looping until the 'n' key is pressed
        while True:
            # display the image and wait for a keypress
            cv2.imshow("inputImage", image)
            key = cv2.waitKey(1) & 0xFF

            # if the 'r' key is pressed, reset the cropping region
            if key == ord("r"):
                image = clone.copy()

            # if the 'c' key is pressed, crop the image
            elif key == ord("c"):
                if len(refPt) == 2:
                    # roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                    binaryImg[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]] = 255
                    filename_w_ext = os.path.basename(file)
                    filename, file_extension = os.path.splitext(filename_w_ext)
                    saveFullPath = '/home/ubuntu/binImages/' + filename + '_label' + file_extension
                    cv2.imwrite(saveFullPath, binaryImg)
            # next image when n pressed
            elif key == ord("n"):
                break
    return 1

if __name__ == "__main__":
    main()
