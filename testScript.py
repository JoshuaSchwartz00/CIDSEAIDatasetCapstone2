import os
import time
import json
import glob

## image generation tests

#image generation script generates 4000+ images
def test1() -> bool:
    image_path_files = glob.glob(os.getcwd() + "\\img\\*.jpg")

    image_count = len(image_path_files)

    return image_count > 4000

#Image generation script generates images with the desired properties/configurations. 
def test2() -> bool:
    pass


## language expression tests

#Language expression generation script generates all possible language expressions for all 4000 generated image scenes. 
def test3() -> bool:
    pass

#Language expression generation script generates valid expressions for all properties in all generated images. 
#(hard to test automatically)
def test4() -> bool:
    pass


## segmentation masking tests

#checks if segmentation mask covers appropriate objects
#(basically impossible to test automatically)
def test5() -> bool:
    pass
    

#checks if the number of segmentation mask images equals the number of language expressions
#checks if the number of segmentation mask images equals the number of images
def test6() -> bool:

    image_path_files = glob.glob(os.getcwd() + "\\img\\*.jpg")
    segmentation_path_files = glob.glob(os.getcwd() + "\\_____\\*.jpg") #seg mask image file

    image_count = len(image_path_files)
    seg_count = len(segmentation_path_files)

    return image_count == seg_count


if __name__ == "__main__":
    #command = "python main.py"
    #os.system(command)
    
    #runs all the tests
    if(test1()):
        print("Test 1 passed.")
    else:
        print("Failure occured in Test 1.")
        
    if(test2()):
        print("Test 2 passed.")
    else:
        print("Failure occured in Test 2.")

    if(test3()):
        print("Test 3 passed.")
    else:
        print("Failure occured in Test 3.")
        
    if(test4()):
        print("Test 4 passed.")
    else:
        print("Failure occured in Test 4.")

    if(test5()):
        print("Test 5 passed.")
    else:
        print("Failure occured in Test 5.")
        
    if(test6()):
        print("Test 6 passed.")
    else:
        print("Failure occured in Test 6.")
    
    #lets the program sleep so it gives it time to finish all the functions and image saving
    #time.sleep(60)

    #removes all the unneeded data
    #os.remove("generated.json")
    #os.rmdir("output")