#!/usr/local/bin/python3
#
# Authors: [Rohit Rokde-rrokde, Bhumika Agrawal-bagrawal, Aastha Hurkat-aahurkat]
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
import copy
import math
import numpy as np
from scipy.ndimage import filters
import sys
import imageio

# calculate "Edge strength map" of an image

def edge_strength(input_image):
    grayscale = np.array(input_image.convert('L'))
    filtered_y = np.zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return np.sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
    
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def bayes(edge_map):
    return(np.argmax(edge_map, axis=0))

def transition(cur_col, prev_idx):
    num_neighbors = 2
    x = num_neighbors*2 + 1
    transition_prob = [1/x if abs(prev_idx-i) <= num_neighbors else 0 for i in range(cur_col.shape[0])]
    return np.asarray(transition_prob)

def viterbi(edge_strength, gt_row=-1, gt_col=-1):

    if gt_row == -1 and gt_col == -1:
        viterbi = np.zeros(edge_strength.shape)
        inital_prob = np.ones((edge_strength.shape[0],1))/edge_strength.shape[0]

        viterbi[:,0] = edge_strength[:,0] * inital_prob[:,0]
        viterbi[:,0]/=sum(viterbi[:,0])
        path = [np.argmax(viterbi[:,0])]
        #loop through columns
        for col in range(1,edge_strength.shape[1]):
            prev_idx = path[-1]
            transition_prob = transition(viterbi[:, col], prev_idx)
            viterbi[:,col] = viterbi[:, col-1] * transition_prob * (edge_strength[:,col]/(np.sum(edge_strength[:,col])) + 1e-6)
            viterbi[:,col]/=np.sum(viterbi[:,col])
            path.append(np.argmax(viterbi[:, col]))
        return path
    else:
        viterbi = np.zeros(edge_strength.shape)
        inital_prob = np.ones((edge_strength.shape[0], 1)) / edge_strength.shape[0]
        viterbi[:, gt_col] = edge_strength[:, gt_col]
        viterbi[gt_row, gt_col] = 1
        viterbi[:, gt_col] /= sum(viterbi[:, gt_col])
        path = [viterbi[gt_row, gt_col]]
        # loop through columns
        for col in range(gt_col + 1, edge_strength.shape[1]):
            prev_idx = path[-1]
            transition_prob = transition(viterbi[:, col], prev_idx)
            viterbi[:, col] = viterbi[:, col - 1] * transition_prob + (
                        edge_strength[:, col] / (np.sum(edge_strength[:, col])) + 1e-6)
            viterbi[:, col] /= np.sum(viterbi[:, col])
            path.append(np.argmax(viterbi[:, col]))

        path_rev = [viterbi[gt_row, gt_col]]
        for col in range( gt_col - 1, -1, -1):
            prev_idx = path_rev[-1]
            transition_prob = transition(viterbi[:, col], prev_idx)
            #print(np.argmax(transition_prob))
            viterbi[:, col] = viterbi[:, col + 1] * transition_prob + (
                        edge_strength[:, col] / (np.sum(edge_strength[:, col])) + 1e-6)
            viterbi[:, col] /= np.sum(viterbi[:, col])
            path_rev.append(np.argmax(viterbi[:, col]))
        path_rev.reverse()
        return  path_rev + path[1:]




# main program
#

(input_filename, gt_row, gt_col) = sys.argv[1:]#("test_images/mountain.jpg", 44, 2)#

# load in image  
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imageio.imwrite( 'edges.jpg', np.uint8(255 * edge_strength / (np.amax(edge_strength))))


path = viterbi(edge_strength, int(gt_row), int(gt_col))
imageio.imwrite('output_simple.jpg', draw_edge(copy.deepcopy(input_image), bayes(edge_strength), (0, 0, 255), 5))
imageio.imwrite('output_map.jpg', draw_edge(copy.deepcopy(input_image), path, (255, 0, 0), 5))
imageio.imwrite('output_human.jpg', draw_edge(copy.deepcopy(input_image),path,(0, 255, 0), 5))