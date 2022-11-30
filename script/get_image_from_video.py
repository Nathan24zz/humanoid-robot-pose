import argparse
import cv2
import os

def getFrame(sec, count, name, videocap): 
    videocap.set(cv2.CAP_PROP_POS_MSEC,sec*1000) 
    hasFrames, image = videocap.read()
    
    if not os.path.exists("./images"): os.makedirs("./images")
    if hasFrames:
        image = cv2.resize(image, (640, 480))
        cv2.imwrite(f'./images/{name}_{count}.jpg', image)     # save frame as JPG file 
    return hasFrames

def convert(dir):
    for x in os.listdir(dir):
        if x.endswith(".mp4"):
            name_video = x.split('.')[0]
            vidcap = cv2.VideoCapture(f'{dir}/{x}')

            sec = 0
            count = 0
            frameRate = 0.25 #it will capture image in each 0.5 second 
            success = getFrame(sec, count, name_video, vidcap) 
            while success: 
                sec = sec + frameRate 
                sec = round(sec, 2)
                count += 1
                success = getFrame(sec, count, name_video, vidcap)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory containing videos that convert to images')
    return parser.parse_args()


def main():
    """Module's main entry point (zopectl.command)."""
    args = parse_args()
    dir = args.dir

    if not os.path.exists(dir):
        raise Exception('Directory does not exist ({0}).'.format(dir))
    convert(dir)

if __name__ == '__main__':
    main()