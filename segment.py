import cv2
import imutils
import numpy as np

LOWER_RED = (np.array([0,120,70]), np.array([10,255,255]))
UPPER_RED = (np.array([170,120,70]), np.array([180,255,255]))
PINK = (np.array([0,91,255]), np.array([0, 142, 255]))
GREEN = (np.array([40,40,40]), np.array([70,255,255]))

def setup_mask(color, img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    total_mask = []
    if color == "red":
        mask1 = cv2.inRange(hsv, LOWER_RED[0], LOWER_RED[1])
        mask2 = cv2.inRange(hsv, UPPER_RED[0], UPPER_RED[1])
        mask3 = cv2.inRange(hsv, PINK[0], PINK[1])
        total_mask = mask1+mask2+mask3
    else:
        total_mask = cv2.inRange(hsv, GREEN[0], GREEN[1])

    #manual brute force normalize binary
    for i in range(len(total_mask)):
        for j in range(len(total_mask[i])):
            if total_mask[i][j] > 0:
                total_mask[i][j] = 255
    
    return total_mask

def remove_contours_closest(contours, ob):
    best_index = -1
    nearest = 999999
    for i in range(len(contours)):
        M = cv2.moments(contours[i])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        dist = abs(ob.location[0] - cX) + abs(ob.location[1] - cY)
        if dist < nearest:
            best_index = i
            nearest = dist
    
    del contours[best_index]

def fill_unnecessary(contours, mask):
    for c in contours:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.floodFill(mask, None, (cX, cY), (0, 0, 0))

def segment(file_location, objects):
    img = cv2.imread(file_location)

    red_mask = setup_mask("red", img)
    green_mask = setup_mask("green", img)

    cnts = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_cnts = imutils.grab_contours(cnts)

    cnts = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_cnts = imutils.grab_contours(cnts)

    for ob in objects:
        if ob.color == "red":
            remove_contours_closest(red_cnts, ob)
        else:
            remove_contours_closest(green_cnts, ob)
        
    fill_unnecessary(red_cnts, red_mask)
    fill_unnecessary(green_cnts, green_mask)

    final_mask = red_mask + green_mask

    res = cv2.bitwise_and(img, img, mask=final_mask)

    return res


def segment_images(sceneList):
    for sc in sceneList:
        for expression in sc.list_expressions:
            #TODO
            


if __name__ == "__main__":
