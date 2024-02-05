import numpy as np
import cv2
import os


for dirname in os.listdir("convertImages/"):

    for filename in os.listdir("convertImages/" + dirname + "/"):

        
        img = cv2.imread("convertImages/" + dirname + "/" + filename, 0)
       

        denoisedImg = cv2.fastNlMeansDenoising(img)
        

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        

        morphImg = cv2.morphologyEx(denoisedImg, cv2.MORPH_CLOSE, kernel, iterations = 2)
        
        
        contours, hierarchy = cv2.findContours(morphImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        

        contoursImg = cv2.cvtColor(morphImg, cv2.COLOR_GRAY2RGB)
        

        cv2.drawContours(contoursImg, contours, -1, (255,100,0), 3)
        #cv2.imshow('final', contoursImg)

        cv2.imwrite("results/" + dirname + "/" + filename + "_result.tif", contoursImg)
        textFile = open("results/results.txt","a")
        textFile.write(filename + " Dots number: {}".format(len(contours)) + "\n")
        textFile.close()
        cv2.waitKey()