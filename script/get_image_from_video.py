import cv2
import os

def getFrame(sec, count, name): 
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000) 
    hasFrames, image = vidcap.read()
    
    if not os.path.exists("./images"): os.makedirs("./images")
    if hasFrames:
        image = cv2.resize(image, (640, 480))
        cv2.imwrite(f'./images/{name}_{count}.jpg', image)     # save frame as JPG file 
    return hasFrames

folder_video = "./videos1"
for x in os.listdir(folder_video):
    if x.endswith(".mp4"):
        name_video = x.split('.')[0]
        vidcap = cv2.VideoCapture(f'{folder_video}/{x}')

        sec = 0
        count = 0
        frameRate = 0.25 #it will capture image in each 0.5 second 
        success = getFrame(sec, count, name_video) 
        while success: 
            sec = sec + frameRate 
            sec = round(sec, 2)
            count += 1
            success = getFrame(sec, count, name_video) 