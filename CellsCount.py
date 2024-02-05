import cv2
import numpy as np
import math

image = cv2.imread("NEUBAUER7_4X-49.jpg")


original = image.copy()
cv2.imshow('original', original)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask1= cv2.inRange(hsv, (0, 30, 0), (20, 255, 200))
mask2= cv2.inRange(hsv, (160, 30, 0), (180, 255, 200))
mask = cv2.bitwise_or(mask1, mask2)
cv2.imshow('mascara', mask)


# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)



# mask1= cv2.inRange(hsv, (0, 30, 20), (90, 255, 255))
# #mask2= cv2.inRange(hsv, (130, 22, 20), (140, 255, 255))

# #mask = cv2.bitwise_or(mask1, mask2)
# cv2.imshow('mascara verdade', mask1)
# target = cv2.bitwise_and(image,image, mask=mask1)
# #cv2.imshow('mascara', target)
# #cv2.imshow('mascara hsv binaria final', target)



# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))

# #close= cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel, iterations=1)
# close2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel, iterations=12)
# cv2.imshow('fechamento de circundancias2', close2)
# cnts = cv2.findContours(close2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# minimum_area = 800
# average_cell_area = 1000
# connected_cell_area = 1500

# cells = 0
# for c in cnts:
#     area = cv2.contourArea(c)

#     if area > minimum_area:
#         cv2.drawContours(original, [c], -1, (0,255,0), 2)
#         if area > connected_cell_area:
#             cells += math.ceil(area / average_cell_area)
#         else:
#             cells += 1
# print('Cells: {}'.format(cells))
# #cv2.imshow('close', close)
# cv2.imshow('original', original)
cv2.waitKey()