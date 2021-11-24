# Capstone 2021: Vlogging MicroDrone
# Computer Vision module

import cv2

def TelloGetFrame(drone):
    myframe = drone.get_frame_read().frame    #get the image
    scale_percent = 60                                  #percent of original size
    width = int(myframe.shape[1]*scale_percent / 100)   #width resized to
    height = int(myframe.shape[0]*scale_percent / 100)  #height resized to
    img = cv2.resize(myframe,(width,height),interpolation=cv2.INTER_AREA)           #resize the image
    return img

def FaceDetection(img):
    faceAlgo = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceAlgo.detectMultiScale(grayImg, 1.1, 5)

    facesCenter = []
    facesArea = []

    for (x,y,w,h) in faces: #w,h dari wajah
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cx = x + w//2; cy = y + h//2; area = w*h;
        facesArea.append(area); facesCenter.append([cx,cy])

    #find the maximum area of rectangle
    if len(facesArea) != 0:
        i = facesArea.index(max(facesArea))
        cv2.circle(img,(int(facesCenter[i][0]),int(facesCenter[i][1])),10,(0,0,255),3) #lingkaran di wajah
        return img, [facesCenter[i],facesArea[i]]
    else:
        return img, [[0,0],0]





