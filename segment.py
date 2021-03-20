import cv2
import imutils
import numpy as np

#RGB bounds for all colors needed to make the segmentation masks
LOWER_RED = (np.array([0,120,70]), np.array([10,255,255]))
UPPER_RED = (np.array([170,120,70]), np.array([180,255,255]))
PINK = (np.array([0,91,255]), np.array([0, 142, 255]))
GREEN = (np.array([40,40,40]), np.array([70,255,255]))

#sets up each of the masks and combines them
def setup_mask(color, img):

    #pulls in the original image and normalizes colors used
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    total_mask = []

    #creates a color mask for whatever color is selected, otherwise objects will end up colored black
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

#removes the closest contour
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

#flood fills unnecessary shapes with black
def fill_unnecessary(contours, mask):
    for c in contours:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.floodFill(mask, None, (cX, cY), (0, 0, 0))

#the start of segmenting the images
def segment(file_location, objects):
    img = cv2.imread(file_location)

    red_mask = setup_mask("red", img)
    green_mask = setup_mask("green", img)

    #finds the contours of the red masks
    cnts = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_cnts = imutils.grab_contours(cnts)

    #finds the contours of the green masks
    cnts = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_cnts = imutils.grab_contours(cnts)

    #depending on what objects we want, delete them from the contours
    for ob in objects:
        if ob.color == "red":
            remove_contours_closest(red_cnts, ob)
        else:
            remove_contours_closest(green_cnts, ob)

    #fill in the contours
    fill_unnecessary(red_cnts, red_mask)
    fill_unnecessary(green_cnts, green_mask)

    final_mask = red_mask + green_mask

    #intersection of image and final mask
    res = cv2.bitwise_and(img, img, mask=final_mask)

    return res

#prototype segmentation mask script for final product 
def segment_images(output_folder, sceneList):
    
    for idx, sc in enumerate(sceneList):
        image_local = sc.image_location
        ob_bank = sc.list_objects
        for idy, expression in enumerate(sc.list_expressions):
            #TODO
            ref_expr, template, obs = expression
            result_img = segment(image_local, obs)
            cv2.imwrite("{}/{}_{}.jpg".format(output_folder, idx, idy), result_img)

            
            


if __name__ == "__main__":
    exit(1)
