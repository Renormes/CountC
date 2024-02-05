import pyautogui
import os
import time



for dirname in os.listdir("C:/countC/images/"):

    for filename in os.listdir("C:/countC/images/" + dirname + "/"):
     
     os.startfile("C:/countC/images/" + dirname + "/" + filename)
     time.sleep(3)
     pyautogui.hotkey("ctrl", "e")
