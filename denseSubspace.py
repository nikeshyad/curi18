import math
import sys

#Display progress bar
def progress(count, total, status = ''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


#Calculate euclidean distance between two n-dimensional points
def euclidDist(point1, point2):
	dist = 0.0
	for i in range(0, len(point1)):
		dist += (point1[i] - point2[i]) ** 2

	return math.sqrt(dist)


# Input: file, the nth nearest point, the percentage of the densest points
# set ripser = True if the output is being used to calculate barcodes with ripser
# set ripser = False if the output is being used with RIVET so that we retain the knn-distance value to use it as a second param

def denseSubspace(filename, outputFile, knn_param, density_param, ripser):

	file = open(filename, "r")

	allPoints = []

	for line in file:
		allPoints.append(line.split())

	#Converting strings to float
	for i in range(0, len(allPoints)):
		for j in range(0, len(allPoints[i])):
			allPoints[i][j] = float(allPoints[i][j])

	#print allPoints

	#dist is a list of distance from a point i to it's n-th nearest neighbor
	dist = []

	total = 49200
	count = 0
	for i in allPoints:
		count += 1
		#tmp is a list of euclidean distances of a point i to all other points j
		tmp = []
		for j in allPoints:
			tmp.append(euclidDist(i,j))

		dist.append(sorted(tmp)[knn_param])

		progress(count, total, status = 'Caclulating euclidean distances')

		#print("Progress: " + str(i/50000.0 * 100) + "%")

	#Appending the n-th nearest neighbor distance to a point (a list) so that the list now contains 10 numbers
	for i in range(0, len(allPoints)):
		allPoints[i].append(dist[i])

	#print dist

	#####################
	# Slice top N% of the distance and store in a list sliced_dist
	# See if the last value of a point (which is the distance value of its n-th nearest neighbor) is contained in sliced_dist
	# If contained in sliced_dist, add the point to topN_densest

	topN_densest = []

	sorted_dist = sorted(dist)
	sliced_dist = sorted_dist[:int(density_param/100.0 * len(sorted_dist))]

	#print sliced_dist

	for i in allPoints:
		if i[len(allPoints[0]) - 1] in sliced_dist:
			topN_densest.append(i)

	######################

	out = open(outputFile, "w")

	#Print the values in topN_densest list
	for i in topN_densest:
		# pop last value to use it with ripser
		if ripser:
			i.pop()

		#print( ", ".join( repr(e) for e in i ) )

		out.write(", ".join(repr(e) for e in i))
		out.write("\n")


denseSubspace("patches_top20", "dense_top20_ripser", 15, 30, ripser = True)
#denseSubspace("test", 5, 50)
