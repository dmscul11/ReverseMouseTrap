import cv2
import numpy as np
# Read the image you want connected components of
src = cv2.imread('F:\\2018 Fall\Courses\Imagery-Based AI\Assignments\Assignment_2\ReverseMouseTrap\loader\images\HARD.png', cv2.CV_8UC1)
# Threshold it so it becomes binary
ret, thresh = cv2.threshold(src,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# You need to choose 4 or 8 for connectivity type
connectivity = 4
# Perform the operation
output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
# Get the results
# The first cell is the number of labels
num_labels = output[0]
# The second cell is the label matrix
labels = output[1]
# The third cell is the stat matrix
stats = output[2]
# The fourth cell is the centroid matrix
centroids = output[3]

for idx in range(len(labels)):
    print(labels[idx])

print(centroids)
print(stats)
print(num_labels)
