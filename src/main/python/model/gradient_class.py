import cv2
import numpy as np


def create_blending(img1, img2):
    G0, M0 = get_weight_mask_matrix(img1, img2)

    weights = [np.stack((G, G, G), axis=2) for G in (G0, G0, G0, G0)]
    end = (img1 * weights[0] + img2 * (1 - weights[0])).astype(np.uint8)
    return end


def get_weight_mask_matrix(im1, im2, dist_threshold=1):
    """
    Get the weight matrix G that combines two images imA, imB smoothly.

    imA = image overlapping A
    imB = image Overlapping B
    """
    overlap_mask = get_overlap_region_mask(im1, im2)
    overlap_mask_inv = cv2.bitwise_not(overlap_mask)
    indices = np.where(overlap_mask == 255)
    # print(indices)
    imA_diff = cv2.bitwise_and(im1, im1, mask=overlap_mask_inv)
    imB_diff = cv2.bitwise_and(im2, im2, mask=overlap_mask_inv)

    G = get_mask(im1).astype(np.float32) / 255.0

    polyA = get_outermost_polygon_boundary(imA_diff)
    polyB = get_outermost_polygon_boundary(imB_diff)

    for y, x in zip(*indices):
        # print(y, x)
        distToB = cv2.pointPolygonTest(polyB, (x, y), True)
        if distToB < dist_threshold:
            distToA = cv2.pointPolygonTest(polyA, (x, y), True)
            distToB *= distToB
            distToA *= distToA
            G[y, x] = distToB / (distToA + distToB)

    return G, overlap_mask


def get_overlap_region_mask(im1, im2):
    """
    Given two images of the save size, get their overlapping region and
    convert this region to a mask array.
    """
    overlap = cv2.bitwise_and(im1, im2)
    mask = get_mask(overlap)
    mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=2)
    return mask


def get_mask(img):
    """
    Convert an image to a mask array.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    return mask


def get_outermost_polygon_boundary(img):
    """
    Given a mask image with the mask describes the overlapping region of
    two images, get the outermost contour of this region.
    """
    mask = get_mask(img)
    mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=2)
    contours, hierarchy = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2:]

    # get the contour with the largest area
    C = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)[0]

    # polygon approximation
    polygon = cv2.approxPolyDP(C, 0.009 * cv2.arcLength(C, True), True)

    return polygon
