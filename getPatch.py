import numpy
import array
import math
import random
from PIL import Image

#list to store contrast values eventually to see histogram of the values
contrast = []

#list to store d_norm contrast values eventually to see histogram of the values
d_norm_contrast = []

NUM_IMAGES = 100
NUM_PATCHES = 100
D_NORM = True

#Function to render a 3 by 3 patch
def render(pixel_list, square_width):
	data = np.zeros((3*square_width, 3*square_width), dtype = np.uint8)
	for i in range(0, square_width):
		for j in range(0, square_width):
			data[i,j] = pixel_list[0]

	for i in range(0, square_width):
		for j in range(square_width, 2*square_width):
			data[i,j] = pixel_list[1]

	for i in range(0, square_width):
		for j in range(2*square_width, 3*square_width):
			data[i,j] = pixel_list[2]

	for i in range(square_width, 2*square_width):
		for j in range(0, square_width):
			data[i,j] = pixel_list[3]

	for i in range(square_width, 2*square_width):
		for j in range(square_width, 2*square_width):
			data[i,j] = pixel_list[4]

	for i in range(square_width, 2*square_width):
		for j in range(2*square_width, 3*square_width):
			data[i,j] = pixel_list[5]

	for i in range(2*square_width, 3*square_width):
		for j in range(0, square_width):
			data[i,j] = pixel_list[6]

	for i in range(2*square_width, 3*square_width):
		for j in range(square_width, 2*square_width):
			data[i,j] = pixel_list[7]

	for i in range(2*square_width, 3*square_width):
		for j in range(2*square_width, 3*square_width):
			data[i,j] = pixel_list[8]

	img = smp.toimage(data)
	img.show()
	return img


#Function to calculate the d-norm contrast of 3 by 3 patches
def d_norm(pixel_list):
	pixel_array = numpy.array(pixel_list)
	pixel_mat = numpy.mat(pixel_array.reshape(9,1))
	pixel_mat_transpose = numpy.mat(pixel_array.reshape(1,9))

	D = numpy.matrix(
	(
		(2, -1, 0, -1, 0, 0, 0, 0, 0),
		(-1, 3, -1, 0, -1, 0, 0, 0, 0),
		(0, -1, 2, 0, 0, -1, 0, 0, 0),
		(-1, 0, 0, 3, -1, 0, -1, 0, 0),
		(0, -1, 0, -1, 4, -1, 0, -1, 0),
		(0, 0, -1, 0, -1, 3, 0, 0, -1),
		(0, 0, 0, -1, 0, 0, 2, -1, 0),
		(0, 0, 0, 0, -1, 0, -1, 3, -1),
		(0, 0, 0, 0, 0, -1, 0, -1, 2)	
		)
	)

	return math.sqrt(pixel_mat_transpose * D * pixel_mat)


#Function to find 100 random 3 by 3 patches from an image
#Returns a list 10 dimensional vectors (3 by 3 patches + d-norm contrast value)
def getPatch(im):
	with open(im, 'rb') as handle:
	   s = handle.read()
	arr = array.array('H', s)
	arr.byteswap()
	img = numpy.array(arr, dtype='uint16').reshape(1024, 1536)

	width = 1024
	height = 1536
	matPixels = [[0 for x in range(height)] for y in range(width)] 

	############
	# Finding a divisor to make the pixels value within range 0-255
	# l = []
	# for i in img:
	# 	l.append(max(i))

	# maxPixel = max(l)

	# divNum = int(math.ceil(maxPixel/255.0))
	############

	#Storing the log value of the pixels in the matrix matPixels
	for i in range(0, width):
		for j in range(0, height):
			
			#img[i][j] = img[i][j]/divNum

			## try log c+1

			try:
				matPixels[i][j] = round(math.log(img[i][j] + 1), 4)
			except:
				print("Log error")

	#print matPixels

	allPatches = []

	#Calculate 100 random 3 by 3 patches
	for i in range(0,NUM_PATCHES):
		rand = random.randint(0+1, width-2)
		#print(rand)
		patch_33 = [matPixels[rand-1][rand+1], matPixels[rand][rand+1], matPixels[rand+1][rand+1], matPixels[rand-1][rand], matPixels[rand][rand], matPixels[rand+1][rand], matPixels[rand-1][rand-1], matPixels[rand][rand-1], matPixels[rand+1][rand-1]]

		max_pixel = max(patch_33)
		min_pixel = min(patch_33)

		#Just to see histogram of contrast values
		contrast.append(max_pixel - min_pixel)
		d_norm_contrast.append(d_norm(patch_33))
		#######

		if D_NORM:
			patch_33.append(d_norm(patch_33))
		else:
			patch_33.append(max_pixel - min_pixel)

		allPatches.append(patch_33)

	return allPatches


#Function to print only the values in the list of patches by stripping the square brackets []
def printPatch(patch):
	for i in patch:
		print(str(i).strip('[]'))


#Print patches. Skip if image is not found. Use output redirection to save patches in a file
for i in range(0,NUM_IMAGES):
	rand = random.randint(1000, 4000)
	im = "Images/imk0" + str(rand) + ".iml"
	#print im
	try:
		printPatch(getPatch(im))
	except:
		continue

# im = Image.fromarray(img, 'L')
# im.show()