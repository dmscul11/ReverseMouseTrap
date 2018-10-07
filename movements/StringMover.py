import numpy as np
import cv2 as cv
import math
import matplotlib.pyplot as plt
from collections import Counter


def pull_string(image, string, direction, pull_end, front_end, back_end):

    new_image = image
    new_string = string
    new_front_end = front_end
    new_back_end = back_end

    return new_image, new_string, new_front_end, new_back_end


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

    print(counts)
    breaking

    return edges, front_end, back_end


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
