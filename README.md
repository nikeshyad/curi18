# CURI 18. Supervisor: Prof. Matthew Wright, St.Olaf College
# Analyzing the behavior of spaces of natural images using persistent homology

Steps:
1. Run getPatch.py and store the output in a file. These are a collection of 100 3 by 3 random patches from each image out of 100 randomly sampled images from the image dataset. (you can specfiy number of images and number of patches to extract by modifying NUM_IMAGES and NUM_PATCHES variables in the code.)
1. Use the R script dimReducePatches.R to filter out the top N% of patches by d-norm contrast, subtract the mean of the patches and divide by d-norm contrast. This will write out a new file.
1. Run denseSubspace.py with the new file as input to find the top N% densest patches with a knn parameter. Use ripser = True flag if the output is being used to calculate barcodes with ripser. If you are using the output with RIVET, we need the knn distance value as a second parameter so use ripser = False flag. A new file is written out as specified in the function parameter.
1. Use the resulting file to calculate barcodes with ripser and store the output in a file: https://github.com/Ripser/ripser
1. Alternatively, use the output and process the file as per requirement of RIVET and visualize barcodes.
1. Run parseRipserOutput.py with the file saved from ripser computation as a command line argument to analyze the outputs from ripser.
