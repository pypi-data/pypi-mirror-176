"""
Copyright 1999 Illinois Institute of Technology

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL ILLINOIS INSTITUTE OF TECHNOLOGY BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of Illinois Institute
of Technology shall not be used in advertising or otherwise to promote
the sale, use or other dealings in this Software without prior written
authorization from Illinois Institute of Technology.
"""

import copy
import cv2
import numpy as np

def getNewZoom(current, move, xmax, ymax, ymin=0):
    """
    Get new zoom location (x, and y ranges) by given current zoom, move vector and x,y maximum ranges
    :param current: current zoom location
    :param move: moving vector
    :param xmax: maximum x
    :param ymax: maximum y
    :param ymin: minimum y
    :return:
    """
    x1 = current[0][0] + move[0]
    x2 = current[0][1] + move[0]
    if x1 < 0:
        x1 = 0
        x2 = current[0][1] - current[0][0]
    if x2 >= xmax:
        x2 = xmax - 1
        x1 = x2 - (current[0][1] - current[0][0])

    y1 = current[1][0] + move[1]
    y2 = current[1][1] + move[1]
    if y1 < ymin:
        y1 = ymin
        y2 = y1 + (current[1][1] - current[1][0])
    if y2 > ymax:
        y2 = ymax
        y1 = y2 - (current[1][1] - current[1][0])

    return [(x1, x2), (y1, y2)]

def rotateImage(img, center, angle, img_type, mask_thres = -999):
    """
    Get rotated image by angle.
    :param img: input image
    :param angle: rotation angle
    :return: rotated image
    """
    if angle == 0:
        return img, center, None

    # M = cv2.getRotationMatrix2D(tuple(center), angle, 1)
    # size = max(img.shape[0], img.shape[1])
    # used for expanding the rotated image
    # im_max_shape = max(img.shape[1], img.shape[0])
    # print("max image shape: {}".format(im_max_shape))
    # im_center = (im_max_shape/2, im_max_shape/2)
    # translation = np.array(im_center) - np.array([img.shape[1]/2, img.shape[0]/2])
    # print(translation)
    # T = np.identity(3)
    # # T[0:1,2] = translation
    # T[0,2] = translation[0]
    # T[1,2] = translation[1]
    # M2 = np.identity(3)
    # print("M: {}".format(M))
    # M2[0:2,:] = M
    # print("M2: {}".format(M2))
    # M3 = np.dot(T, M2)
    # print("M3: {}".format(M3))
    # M1 = M3[0:2,:]
    # print("M1: {}".format(M1))

    if img_type == "PILATUS":
        img = img.astype('float32')
        if mask_thres == -999:
            mask_thres = getMaskThreshold(img, img_type)
        mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        mask[img <= mask_thres] = 255
        rotated_img, center, rotMat = rotateNonSquareImage(img, angle, center)
        rotated_mask, _, _ = rotateNonSquareImage(mask, angle, center)
        rotated_mask[rotated_mask > 0.] = 255
        rotated_img[rotated_mask > 0] = mask_thres
        return rotated_img, center, rotMat
    else:
        return rotateNonSquareImage(img, angle, center)

def getMaskThreshold(img, img_type):
    """
    Compute the mask threshold for the image given
    :param img, img_type:
    :return: mask threshold
    """
    min_val = img.min()
    if min_val < 0:
        mask_thres = -0.01
    else:
        mask_thres = min_val
    if img_type == "PILATUS":
        hist = np.histogram(img, 3, (min_val, min_val+3))
        max_ind = np.argmax(hist[0])
        mask_thres = hist[1][max_ind]
    return mask_thres

def rotateNonSquareImage(img, angle, center1):
    """
    Rotates a non square image by first determining the appropriate square image and then rotating the image.
    :param file_list: original non square image, angle of rotation and center
    :return: rotated image and center with respect to new coordinate system
    """
    height, width = img.shape
    center = (width/2, height/2)

    rotation_mat = cv2.getRotationMatrix2D(center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - center[0]
    rotation_mat[1, 2] += bound_h/2 - center[1]

    maxB = max(bound_h, bound_w)

    center1 = [center1[0], center1[1], 1]
    center1 = np.dot(rotation_mat, center1)
    center2 = (int(center1[0]), int(center1[1]))

    # rotate image with the new bounds and translated rotation matrix
    rotated_img = cv2.warpAffine(img, rotation_mat, (maxB, maxB))
    return rotated_img, center2, rotation_mat
