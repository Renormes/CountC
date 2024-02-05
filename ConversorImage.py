import os
import numpy as np
import cv2


i = 1
for dirname in os.listdir("C:/countC/images/"):

    for filename in os.listdir("C:/countC/images/" + dirname + "/"):
        ft = cv2.imread("C:/countC/images/" + dirname + "/" + filename)
        hsv = cv2.cvtColor(ft, cv2.COLOR_BGR2HSV)
        mask1= cv2.inRange(hsv, (0, 40, 0), (20, 255, 200))
        mask2= cv2.inRange(hsv, (160, 40, 0), (180, 255, 200))
        mask = cv2.bitwise_or(mask1, mask2)
        path = 'C:/countC/convertImages/conversions'
        cv2.imwrite(os.path.join(path , filename), mask)
        