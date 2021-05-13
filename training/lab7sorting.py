"""
lab7sorting.py

Author: Cynthia Hom
Date: Spring 2021

lab7sorting.py opens up the csv and makes a bunch of images in the images folder,
one for each row of the csv. The images' names are "x.jpg", where
x is the index of the row in the dataframe.

After running this script on the Kaggle csv, I manually picked out 
5 specific people to use as the validation dataset by dragging and 
dropping their image files into a single validation folder. I then
ran lab7valid.py to create a csv file that contained a 1 for every
row in the csv that was a validaiton image (i.e. one of the images in the 
validation folder) and a 0 otherwise.

This file was necessary because the Kaggle data had the same people
repeated in the training data, without any "person id" to identify which 
people occured in which rows of the dataframe. Without this, we would have
leaking between the training and validation sets, since the same people would
be in both sets. This would give us an artificially low validation loss metric.
"""

import pandas as pd 
import numpy as np 
from PIL import Image
from pathlib import Path

# Open csv
df = pd.read_csv("training.csv")

# Reshape values in 'Image' column. This function is copied over from
# "FacialFeatures.ipynb".
IMG_SHAPE = (96, 96)

def stringToArr(stringIn):
  return np.array([float(value) for value in stringIn.split(' ')]).reshape(IMG_SHAPE)

df['Image'] = df['Image'].map(stringToArr)


# Drop nan values and check length
df = df.dropna()
print("length of dataframe is ", len(df['Image']))
print("and it should be 2140")

# Loop through, make images, save in "images" directory
# "df.index" gives an iterable that corresponds to the dataframe row 
#  indicies.
for i in df['Image'].index:
	img = Image.fromarray(df['Image'][i].astype(np.uint8))
	img.save(Path("images")/f"{i}.jpg")