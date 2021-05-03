"""
Contains the code for applying the filter.
Author: Cynthia Hom
TODO: update requriemnts .txt
TODO: change to only keep filter location not frame itself
"""

from fastai import *
from fastai.vision.all import *
import cv2
import imutils
# Include so that learner knows what get_y is.

#CARD_WIDTH_TO_HEIGHT_RATIO = 2.5/3.5

def get_y(r):
	return [
    [r['left_eyebrow_outer_end_x'], r['left_eyebrow_outer_end_y']],
    [r['right_eyebrow_outer_end_x'], r['right_eyebrow_outer_end_y']],
    [r['nose_tip_x'], r['nose_tip_y']],
    ]


class Filter():
	def __init__(self):
		self.learn = load_learner('./models/kaggle1.pkl')
		# path to cardImgs data
		self.cardImgs = untar_data('http://web2.acbl.org/documentlibrary/marketing/Clip_Art/cards_png_zip.zip')
		#path = cardImgs/"AS.png"
		self.spadeAce = PILImage.create(self.cardImgs/"AS.png") # TODO: later change to do all cards.
		self.filterImage = self.spadeAce # set filter image to be spadeAce for now.
		#self.currFrame = np.zeros((480, 640, 3)) # initialize to something random TODO: maybe change.
		#cascPath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
		self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
		#self.btwnEyebrows = TensorPoint([0, 0])
		# nose  = TensorPoint([0, 0])
		# self.cardHeight = 10
		# self.toMult = np.zeros((480, 640, 3))
		# self.toAdd = np.zeros((480, 640, 3))
		self.rotatedResizedFilter = np.zeros((480, 640, 3))
		self.inverseBinary = np.zeros((480, 640, 3))
		self.startX, self.startY, self.endX, self.endY = (0, 0, 0, 0)
		self.startXC, self.startYC, self.endXC, self.endYC = (0, 0, 0, 0)




	def applyFilter(self, img, timeStep):#, self.filterImg, learn):
		"""
		img: PILImage, image to put filter on
		"""
		#oldImg = img
		#print("oldImg shape is", oldImg.shape)
		# Create images
		#img = np.array(PILImage.create(imgName))
		#self.filterImg = PILImage.create(imgFilterPath)
		#print("type if img is ", type(img))
		if timeStep % 20 == 0:
			img = np.array(img)
			tensorPoints = self.getTensorPoints(img)#, self.learn)

			# calculate position of filter
			btwnEyebrows = (tensorPoints[0] + tensorPoints[1])/2
			# xBtwnEyebrows = int(btwnEyebrows[0]) # (x, y) is point of bottom middle of playing card
			# yBtwnEyebrows = int(btwnEyebrows[1])

			nose = tensorPoints[2]

			# Calculate card width and height
			# Card height is about twice distance between btwnEyebrows and nose
			cardHeight = int(2*np.sqrt(sum(np.square(btwnEyebrows - nose))))
			# if (cardHeight > yBtwnEyebrows): # TODO: make sure this didnt break anything, also update in colab code.
			# 	cardHeight = yBtwnEyebrows # Don't let the starting position be negative.
			#cardWidth = CARD_WIDTH_TO_HEIGHT_RATIO * cardHeight
			# if (cardWidth/2 > xBtwnEyebrows):
			# 	cardWidth = xBtwnEyebrows*2 # Don't let the starting position be negative.

			# Overlay the filter
			self.getFilterFrame(cardHeight, btwnEyebrows, nose)
			# ctxImg = TensorImage(self.currFrame).show() # show the scaled points on the original image.
			# tensorPoints.show(ctx=ctxImg);
		# # create final image
		finalImg = self.applyFilterFrame(img)
		#finalImg = (np.array(img) * self.toMult + self.toAdd).astype('uint8')
		return finalImg#self.currFrame#oldImg#self.currFrame

	def getTensorPoints(self, img):#, learn):
		#NOTE: imgName parameter is just so that we can say if there was no face found for a particular image.
		# Get only the face, and account for the case where no face is found.

		faces = []#self.faceCascade.detectMultiScale(img, minNeighbors=3, minSize=(int(img.shape[0]/10), int(img.shape[0]/10)))
		if len(faces) > 1:
			print("faces greater than 1 ")# + imgName)
		if len(faces) != 0:
			x,y,w,h = faces[0]
			onlyFaceImg = img[y:y + h, x:x + w]
		else:
			x = 0; y = 0; h, w = img.shape[:2]
			onlyFaceImg = img
			print("no face found ")# + imgName)
		#cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Uncomment to show rectangle

		# Get tensor points
		grayscaleImg = np.array(PILImage.create(onlyFaceImg).convert('L').resize((96, 96)))
		tensorPointsGrayscale = self.learn.predict(grayscaleImg)[0]

		# Adjust tensor points for original image size. Slice off first two parts of shape.
		ratios = tensor(onlyFaceImg.shape[:2])/tensor([96, 96])
		ratios = tensor(ratios[1], ratios[0]) # swap because in TensorPoints, first is column index, second is row index (x, y)
		# Multiply by ratios and add x, y since tensor points are based on cropped face only image.
		return ratios * tensorPointsGrayscale + tensor(x, y)

	def getFilterFrame(self, filterHeight, btwnEyebrows, nose):
		"""
		img: PILImage, image to put the filter over
		filterHeight: double, the height of the filter
		btwnEyebrows: TensorPoint, contains x, y of the midpoint of the eyebrows
		nose: TensorPoint, contains x, y of the tip of the nose
		"""
		yBtwnEyebrows = int(btwnEyebrows[1])#189
		xBtwnEyebrows = int(btwnEyebrows[0])#138
		# change in x/change in y , nose first
		difference = nose - btwnEyebrows#np.array([xBtwnEyebrows, yBtwnEyebrows])
		angle = float(-np.arctan(difference[0]/difference[1]) * 180.0/np.pi)
		#print(angle)
		# calculations
		resizeRatio = filterHeight/self.filterImage.shape[0]
		filterWidth = int(self.filterImage.shape[1]*resizeRatio)
		resizedFilter = self.filterImage.resize((filterWidth, filterHeight)) # width then height
		self.rotatedResizedFilter = imutils.rotate_bound(np.array(resizedFilter), angle=angle)#imutils.rotate_bound(np.array(self.filterImage), angle=45)

		# use to black out parts of original image
		binaryCard = np.zeros(np.array(resizedFilter).shape) + 1
		rotatedBinary = imutils.rotate_bound(binaryCard, angle=angle)#imutils.rotate_bound(np.array(self.filterImage), angle=45)
		self.inverseBinary = (rotatedBinary < 1).astype(int)

		# Calculate positions
		# starting x and y for upper left corner of filter
		self.endX = int(xBtwnEyebrows + filterWidth/2 * np.cos(-angle*np.pi/180))
		self.endY = int(yBtwnEyebrows + filterWidth/2 * np.sin(-angle*np.pi/180)) # use trig
		self.startY = self.endY - self.inverseBinary.shape[0]
		self.startX = self.endX - self.inverseBinary.shape[1]

		# indicies for the card itself.
		self.startYC = 0; self.endYC = self.inverseBinary.shape[0]; self.startXC = 0; self.endXC = self.inverseBinary.shape[1]

	def applyFilterFrame(self, img):
		# Adjust for edge cases
		if (self.startY < 0): # top
			self.startYC = abs(self.startY)
			self.startY = 0
		if (self.startX < 0): # left
			self.startXC = abs(self.startX)
			self.startX = 0
		if (self.endY > img.shape[0]): # bottom
			self.endYC = self.endY - img.shape[0]
			self.endY = img.shape[0]
			#print("updating end y")
		if (self.endX > img.shape[1]): # right
			self.endXC = self.endX - img.shape[1]
			self.endX = img.shape[1]

		# create image to multiply by to black out filter area
		toMult = np.ones(np.array(img).shape)
		toMult[self.startY:self.endY, self.startX:self.endX,:] = self.inverseBinary[self.startYC:self.endYC, self.startXC:self.endXC, :]

		# create image to add to put in filter
		toAdd = np.zeros(np.array(img).shape)
		toAdd[self.startY:self.endY, self.startX:self.endX,:] = self.rotatedResizedFilter[self.startYC:self.endYC, self.startXC:self.endXC, :]
		finalImg = (np.array(img) * toMult + toAdd).astype('uint8')
		# # create final image
		# finalImg = (np.array(img) * self.toMult + self.toAdd).astype('uint8')
		return finalImg # Must be type uint8 for things to work.


		#img
	# def applyFilter(self, imgArr):#, learn): # TODO: finish. Same as colab
	#     print("inside applyFilter")
	#     #imgArr = np.array(imgArr)
	#     img = PILImage.create(imgArr)
	#     grayscaleImg = np.array(img.convert('L').resize((96, 96)))
	#     tensorPointsGrayscale = self.learn.predict(grayscaleImg)[0] # TODO: figure out why predicted points aren't right??    
	#     #print(tensorPoints[0])
	#     #print(tensorPoints[1])
	#     #print(tensorPoints[2])
	#     ratios = tensor(img.shape)/tensor([96, 96])
	#     ratios = tensor(ratios[1], ratios[0]) # swap because in TensorPoints, first is column index, second is row index (x, y)
	#     tensorPoints = ratios * tensorPointsGrayscale
	#     btwnEyebrows = (tensorPoints[0] + tensorPoints[1])/2
	#     #print(int(btwnEyebrows[0]))
	#     x = int(btwnEyebrows[0]) # (x, y) is point of bottom middle of playing card
	#     y = int(btwnEyebrows[1])
	    
	#     return x - 20, x - 20, x + 20, x + 20, y - 30, y, y,y - 30
	#     #y - 30: y, x - 20: x + 20#imgArr
