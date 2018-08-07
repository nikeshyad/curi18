# Command line program to parse the barcode outputs from ripser
# ./parseRipserOutput.py ripser_output_file 
# Prints the length of barcodes in sorted order
# Prints the sorted list of consecutive differences of barcode length

import sys
filename = sys.argv[1]

file = open(filename, "r")

dim0 = False
dim1 = False
dim2 = False

list_dim0 = []
list_dim1 = []
list_dim2 = []

for line in file:
	l = line.lstrip(' [ ').replace(',', ' ').replace(')', '').split()
	if "point" in l or "distance" in l or "value" in l:
		#print "skipping first 3 lines"
		continue
	#print l
	if '0:' in l:
		#print "dim 0"
		dim0 = True
		continue
	if "1:" in l:
		#print "dim 1" 
		dim0 = False
		dim1 = True
		continue
	if "2:" in l:
		#print "dim 2"
		dim1 = False
		dim2 = True
		continue
		
	else:
		try:
			diff = float(l[1]) - float(l[0])
		except:
			diff = "infinite bar"
		#print diff

		if dim0:
			list_dim0.append(diff)

		if dim1:
			list_dim1.append(diff)

		if dim2:
			list_dim2.append(diff)

print "dim0\n", sorted(list_dim0), "\n"

print "dim1\n", sorted(list_dim1), "\n"

print "sorted consecutive differences"
print sorted([t - s for s, t in zip(sorted(list_dim1), sorted(list_dim1)[1:])]), "\n"

print "dim2\n", sorted(list_dim2), "\n"

print "sorted consecutive differences"
print sorted([t - s for s, t in zip(sorted(list_dim2), sorted(list_dim2)[1:])])
