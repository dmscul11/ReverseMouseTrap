import numpy as np
import cv2 as cv
import math
import matplotlib.pyplot as plt
from collections import Counter


def pull_string(image, string, pull_end, front_end, pull_dir, back_end, width):

    # passes objects[string object index]
    # coords = string.get_coordinates()
    # color = string.get_color().decode('UTF-8')
    # first_pixel = [coords[0][0], coords[0][1]]
    coords = list(string)
    new_string = list(coords)

    # delete back end pixels and add line to front end
    if pull_end == 'front':

        # find frontier to create new line of pixels
        most_left = 100000
        if pull_dir == 'up':
            start_row = 100000
        elif pull_dir == 'down':
            start_row = 0
        for f in front_end:
            if f[1] < most_left:
                most_left = f[1]
            if pull_dir == 'up':
                if f[0] < start_row:
                    start_row = f[0]
            elif pull_dir == 'down':
                if f[0] > start_row:
                    start_row = f[0]

        # update front (added line of width) pixels
        new_front_end = []
        for i in range(width):
            if pull_dir == "up":
                new_front_end.append((start_row - 1, most_left + i))
                new_string.append((start_row - 1, most_left + i))
                image[start_row - 1, most_left + i, :] = [0., 128., 0.]
            elif pull_dir == "down":
                new_front_end.append((start_row + 1, most_left + i))
                new_string.append((start_row + 1, most_left + i))
                image[start_row + 1, most_left + i, :] = [0., 128., 0.]

        # update new back end (green pixels touching deleted pixels)
        new_back_end = []
        for bp in back_end:
            for j in range(1, 2):
                if ((bp[0] + j, bp[1]) in string) and ((bp[0] + j, bp[1]) not in new_back_end):
                    new_back_end.append((bp[0] + j, bp[1]))
                if ((bp[0] - j, bp[1]) in string) and ((bp[0] - j, bp[1]) not in new_back_end):
                    new_back_end.append((bp[0] - j, bp[1]))
                if ((bp[0], bp[1] + j) in string) and ((bp[0], bp[1] + j) not in new_back_end):
                    new_back_end.append((bp[0], bp[1] + j))
                if ((bp[0], bp[1] - j) in string) and ((bp[0], bp[1] - j) not in new_back_end):
                    new_back_end.append((bp[0], bp[1] - j))
                if ((bp[0] + j, bp[1] + j) in string) and ((bp[0] + j, bp[1] + j) not in new_back_end):
                    new_back_end.append((bp[0] + j, bp[1] + j))
                if ((bp[0] + j, bp[1] - j) in string) and ((bp[0] + j, bp[1] - j) not in new_back_end):
                    new_back_end.append((bp[0] + j, bp[1] - j))
                if ((bp[0] - j, bp[1] + j) in string) and ((bp[0] - j, bp[1] + j) not in new_back_end):
                    new_back_end.append((bp[0] - j, bp[1] + j))
                if ((bp[0] - j, bp[1] - j) in string) and ((bp[0] - j, bp[1] - j) not in new_back_end):
                    new_back_end.append((bp[0] - j, bp[1] - j))

            # remove old back end pixels from string coords and make blue in image
            new_string = list(value for value in new_string if value != bp)
            image[bp[0], bp[1], :] = [255., 255., 255.]
        new_back_end = list(set(new_back_end))

    # delete front end pixels and add line to back end
    else:

        # find frontier to create new line of pixels
        most_left = 100000
        if pull_dir == 'up':
            start_row = 100000
        elif pull_dir == 'down':
            start_row = 0
        for f in back_end:
            if f[1] < most_left:
                most_left = f[1]
            if pull_dir == 'up':
                if f[0] < start_row:
                    start_row = f[0]
            elif pull_dir == 'down':
                if f[0] > start_row:
                    start_row = f[0]

        # update front (added line of width) pixels
        new_back_end = []
        for i in range(width):
            if pull_dir == "up":
                new_back_end.append((start_row - 1, most_left + i))
                new_string.append((start_row - 1, most_left + i))
                image[start_row - 1, most_left + i, :] = [0., 128., 0.]
            elif pull_dir == "down":
                new_back_end.append((start_row + 1, most_left + i))
                new_string.append((start_row + 1, most_left + i))
                image[start_row + 1, most_left + i, :] = [0., 128., 0.]

        # update new front end (green pixels touching deleted pixels)
        new_front_end = []
        for bp in front_end:
            for j in range(1, 2):
                if ((bp[0] + j, bp[1]) in string) and ((bp[0] + j, bp[1]) not in new_front_end):
                    new_front_end.append((bp[0] + j, bp[1]))
                if ((bp[0] - j, bp[1]) in string) and ((bp[0] - j, bp[1]) not in new_front_end):
                    new_front_end.append((bp[0] - j, bp[1]))
                if ((bp[0], bp[1] + j) in string) and ((bp[0], bp[1] + j) not in new_front_end):
                    new_front_end.append((bp[0], bp[1] + j))
                if ((bp[0], bp[1] - j) in string) and ((bp[0], bp[1] - j) not in new_front_end):
                    new_front_end.append((bp[0], bp[1] - j))
                if ((bp[0] + j, bp[1] + j) in string) and ((bp[0] + j, bp[1] + j) not in new_front_end):
                    new_front_end.append((bp[0] + j, bp[1] + j))
                if ((bp[0] + j, bp[1] - j) in string) and ((bp[0] + j, bp[1] - j) not in new_front_end):
                    new_front_end.append((bp[0] + j, bp[1] - j))
                if ((bp[0] - j, bp[1] + j) in string) and ((bp[0] - j, bp[1] + j) not in new_front_end):
                    new_front_end.append((bp[0] - j, bp[1] + j))
                if ((bp[0] - j, bp[1] - j) in string) and ((bp[0] - j, bp[1] - j) not in new_front_end):
                    new_front_end.append((bp[0] - j, bp[1] - j))

            # remove old front end pixels from string coords and make blue in image
            new_string = list(value for value in new_string if value != bp)
            image[bp[0], bp[1], :] = [255., 255., 255.]
        new_front_end = list(set(new_front_end))

    return image, new_string, new_front_end, new_back_end


# check which end of string object moving is pulling the string
def end_check(object, string, front_end, back_end):

    # get COM of object

    # if COM closer to first front_end pixel
    end = 'front'

    # otherwise COM closer to back_end pixel

    return end


# need the edge information to find the width, and need the string
# ends in order to continually update string, but both
# only need to be found once in the beginning and recorded/updated
def get_string_ends(string, color_matrix):

    # passes objects[string object index]
    # coords = string.get_coordinates()
    # color = string.get_color().decode('UTF-8')
    # first_pixel = [coords[0][0], coords[0][1]]
    coords = string

    # find end pixels of string
    edges = []
    for p in coords:

        # count up neighboring pixels not green
        count = 0
        if color_matrix[(p[0] - 1, p[1])].decode('UTF-8') != 'g':
            count = count + 1
        if color_matrix[(p[0] + 1, p[1])].decode('UTF-8') != 'g':
            count = count + 1
        if color_matrix[(p[0], p[1] + 1)].decode('UTF-8') != 'g':
            count = count + 1
        if color_matrix[(p[0], p[1] - 1)].decode('UTF-8') != 'g':
            count = count + 1
        if color_matrix[(p[0] - 1, p[1] + 1)].decode('UTF-8') != 'g':
            count = count + 1
        if color_matrix[(p[0] - 1, p[1] - 1)].decode('UTF-8') != 'g':
            count = count + 1
        if color_matrix[(p[0] + 1, p[1] + 1)].decode('UTF-8') != 'g':
            count = count + 1
        if color_matrix[(p[0] + 1, p[1] - 1)].decode('UTF-8') != 'g':
            count = count + 1

        # if has 4 or more neighbors then is a corner or edge
        if count >= 4:
            edges.append(p)

    # find edge pixels with most closest other edge pixels nearby
    counts = []
    for e in edges:
        cnt = 0

        for i in range(10):
            if (e[0] + i, e[1] + i) in edges:
                cnt = cnt + 1
            if (e[0] + i, e[1] - i) in edges:
                cnt = cnt + 1
            if (e[0] - i, e[1] + i) in edges:
                cnt = cnt + 1
            if (e[0] - i, e[1] - i) in edges:
                cnt = cnt + 1
            if (e[0] + i, e[1]) in edges:
                cnt = cnt + 1
            if (e[0] - i, e[1]) in edges:
                cnt = cnt + 1
            if (e[0], e[1] + i) in edges:
                cnt = cnt + 1
            if (e[0], e[1] - i) in edges:
                cnt = cnt + 1
        counts.append(cnt)

    # find max counts pixels
    top = sorted(np.unique(counts), reverse=True)[:2]
    top_idx = np.nonzero((counts == top[0]) ^ (counts == top[1]))
    ends = [edges[i] for i in top_idx[0]]

    # find pixel closest to top left as front
    distances = []
    for e in ends:
        dist = int(round(math.sqrt((e[0] - 0)**2 + (e[1] - 0)**2)))
        distances.append(dist)
    min_dist = min(distances)
    min_idx = distances.index(min_dist)
    min_pixel = ends[min_idx]

    # separate into front and back
    front_end = []
    back_end = []
    for e in ends:
        dist = math.sqrt((e[0] - min_pixel[0])**2 + (e[1] - min_pixel[1])**2)
        if dist < 50:
            front_end.append(e)
        else:
            back_end.append(e)

    return edges, front_end, back_end


# need width in order to continually update string
def get_string_width(edges):

    distances = []
    for p1 in edges:
        for p2 in edges:

            # get distances only between relatively close pixels
            if ((p2[0] - p1[0]) < 30 & (p2[1] - p1[1]) < 30):
                dist = int(round(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)))
                if dist < 50:
                    distances.append(dist)

    modes = Counter(distances).most_common(5)

    width = modes[0][0]

    return width
