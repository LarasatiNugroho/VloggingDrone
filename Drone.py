

#module lama
#from module_2d import *

#module baru
from tello_cv import *
from tello_control import *

import time

counter = 0
drone = connectingTello()                       #as the name stated
while True:
    #drone takes flight
    if counter == 0:
        time.sleep(5)       #wait 5 secks
        #drone.takeoff()
        counter == 1

    img = TelloGetFrame(drone)              #Capture picture from the drone's camera
    img,info= FaceDetection(img)               #Detect a face in the image; info shows [cx,cy] and [area face rectangle]
    velocity_maju,velocity_yaw,velocity_up = TrackFace(drone,info,img)     #FaceTracking

    #shows the screen
    cv2.imshow("Screen", img)

    # stop when press "k"
    if cv2.waitKey(1) & 0xFF == ord('k'):
        #drone.land()
        break

cv2.destroyAllWindows()