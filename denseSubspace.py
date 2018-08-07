import math

#Calculate euclidean distance between two n-dimensional points
def euclidDist(point1, point2):
	dist = 0.0
	for i in range(0, len(point1)):
		dist += (point1[i] - point2[i]) ** 2

	return math.sqrt(dist)


#Input: file, the nth nearest point, the percentage of the densest points
#Returns: 9 dimensional vectors 
def denseSubspace(filename, knn_param, density_param):

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

	for i in allPoints:
		#tmp is a list of euclidean distances of a point i to all other points j
		tmp = []
		for j in allPoints:
			tmp.append(euclidDist(i,j))
		#print sorted(tmp)
		#print sorted(tmp)[knn_param]
		dist.append(sorted(tmp)[knn_param])

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


	#Print the values in topN_densest list
	for i in topN_densest:
		i.pop()
		print( ", ".join( repr(e) for e in i ) )


denseSubspace("patches_top20_sample5", 15, 30)
#denseSubspace("test", 5, 50)
