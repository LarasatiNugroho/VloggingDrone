from tello_cv import *
from tello_control import *
import time

#start here
counter = 0
drone = connectingTello()                       #as the name stated

#hover drone
time.sleep(5)
drone.takeoff()
time.sleep(3)
drone_height = drone.get_height()
print(f"my height is {drone_height}")
drone.move_up(int(150-drone_height))

while True:
    img = TelloGetFrame(drone)              #Capture picture from the drone's camera
    img,info= FaceDetection(img)               #Detect a face in the image; info shows [cx,cy] and [area face rectangle]
    velocity_maju,velocity_yaw,velocity_up = TrackFace(drone,info,img)     #FaceTracking

    #shows the screen
    cv2.imshow("Screen", img)

    # stop when press "k"
    if cv2.waitKey(1) & 0xFF == ord('k'):
        drone.land()
        break

drone.streamoff()
cv2.destroyAllWindows()

#ini revisi takeoffnya nggak loop