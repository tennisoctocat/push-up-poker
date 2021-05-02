"""
Contains the code for applying the filter.
Author: Cynthia Hom
"""

from fastai import *
from fastai.vision.all import *
# Include so that learner knows what get_y is.
def get_y(r):
	return [
    [r['left_eyebrow_outer_end_x'], r['left_eyebrow_outer_end_y']],
    [r['right_eyebrow_outer_end_x'], r['right_eyebrow_outer_end_y']],
    [r['nose_tip_x'], r['nose_tip_y']],
    ]


class Filter():
	def __init__(self):
		self.learn = load_learner('./models/kaggle1.pkl')


	def applyFilter(self, imgArr):#, learn): # TODO: finish. Same as colab
	    print("inside applyFilter")
	    #imgArr = np.array(imgArr)
	    img = PILImage.create(imgArr)
	    grayscaleImg = np.array(img.convert('L').resize((96, 96)))
	    tensorPointsGrayscale = self.learn.predict(grayscaleImg)[0] # TODO: figure out why predicted points aren't right??    
	    #print(tensorPoints[0])
	    #print(tensorPoints[1])
	    #print(tensorPoints[2])
	    ratios = tensor(img.shape)/tensor([96, 96])
	    ratios = tensor(ratios[1], ratios[0]) # swap because in TensorPoints, first is column index, second is row index (x, y)
	    tensorPoints = ratios * tensorPointsGrayscale
	    btwnEyebrows = (tensorPoints[0] + tensorPoints[1])/2
	    #print(int(btwnEyebrows[0]))
	    x = int(btwnEyebrows[0]) # (x, y) is point of bottom middle of playing card
	    y = int(btwnEyebrows[1])
	    
	    return x - 20, x - 20, x + 20, x + 20, y - 30, y, y,y - 30
	    #y - 30: y, x - 20: x + 20#imgArr
