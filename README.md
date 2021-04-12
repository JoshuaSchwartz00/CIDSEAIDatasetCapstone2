# CIDSEAIDatasetCapstone2

This file describes how to run the VRE dataset creation script.
Arizona State University Senior Capstone Project
Team Name: CIDSE Large-Scale Dataset Creation for Artificial Intelligence (AI) Research
Team Members: Autumn Martin, Branden Roper, Jack Summers, Joshua Schwartz, Ricky Hsu, Wei Chen

Script file name = main.py

## Prerequisites

To use the scripts, you need to install some additional libraries. Please run the following pip installations below.

pip install -u pillow

pip install -u vpython

pip install -u opencv-python

pip install -u numpy


## Instructions

In commandline, you run "python main.py". It will open a web browser and begin generating images while taking pictures of the screen. During this process the browser must not be touched and the mouse must not be moved into the boxed area. Afterwards, the script will generate all the language expressions for each image. Then a segmentation mask is created for each image according to the language expression. The original images will be stored in the img file, the segmentation mask images will be stored in the segmentation_mask_images file, and the output containing the image names and language expressions will be stored in generated.json.

## Output

Output file name = generated.json

Original images file: /img/

Segmentation mask images file: /segmentation_mask_images/




To use the classes:

```python
from data import *

print(Object)
print(Scene)
print(list_scenes)
```
