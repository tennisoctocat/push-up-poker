"""
valid.py

Author: Cynthia Hom
Date: Spring 2021

Another script, sorting.py, opens up the csv and makes a
bunch of images in the images folder,
one for each row of the csv. The images' names are "x.jpg", where
x is the index of the row in the dataframe.

After running this script on the Kaggle csv, I manually picked out 
5 specific people to use as the validation dataset by dragging and 
dropping their image files into a single validation folder. 

I then ran this file, valid.py to create a csv file that contained a 1 for every
row in the csv that was a validaiton image (i.e. one of the images in the 
validation folder) and a 0 otherwise.

This file was necessary because the Kaggle data had the same people
repeated in the training data, without any "person id" to identify which 
people occured in which rows of the dataframe. Without this, we would have
leaking between the training and validation sets, since the same people would
be in both sets. This would give us an artificially low validation loss metric.
"""

import os
import csv

# Set of dataframe rows that are in validation set
isValid = {}

path = "."
NUM_OF_ROWS = 2140

# Loop through all files in this directory.
AllFiles = list(os.walk(path))
data = []
for item in AllFiles:
	_, _, LoFiles = item 
	for fileName in LoFiles:
		isValid.add(int(fileName[:-4])) # .jpg is the file path for all files
		print("adding",int(fileName[:-4]), "to the set")

with open('isValid.csv', 'w', newline='') as csvfile:
	# Make the writer
	writer = csv.writer(csvfile)
	print("writing")
	# Write one row per tuple. Write 1 if in validation set, 0 otherwise
	for i in range(NUM_OF_ROWS)
		writer.writerow([str(int(i in isValid))])
