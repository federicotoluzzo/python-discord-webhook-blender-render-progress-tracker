import cv2
import pyautogui
from dhooks import Webhook, Embed
import time
import PIL.Image
import os
import pytesseract

hook = Webhook('INSERT WEBHOOK URL HERE')

render_box = (0, 48, 1920, 70)
class aNameForMyClass():
    def __init__(self):
        while True:
            time.sleep(5)
            self.sendInfo(self.getInfo())
            
    def sendInfo(self, info):
        embed = Embed(description=f'current render status : {info}', color=0xFFA200, timestamp='now')
        hook.send(embed=embed)
    
    def getInfo(self):
        #os.remove('info.png')
        phrase = ""
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('text.png')
        img = PIL.Image.open('text.png')
        img2 = img.crop(render_box)
        img2.save('info.png')
        img = cv2.imread('info.png')
        config = ('-l eng --oem 1 --psm 3')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, threshimg = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        dilation = cv2.dilate(threshimg, rect_kernel, iterations = 1)
        img_contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in img_contours: 
            x, y, w, h = cv2.boundingRect(cnt) 
            rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            cropped_img = img[y:y + h, x:x + w] 
            file = open("recognized.txt", "a")
            text = pytesseract.image_to_string(cropped_img)
            phrase = phrase + text
        return phrase

aNameForMyClass()
