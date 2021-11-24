# Capstone 2021: Vlogging MicroDrone
# Control module

from djitellopy import Tello
import numpy as np
import cv2

def connectingTello():

    drone = Tello()     #defined that drone is tello
    drone.connect()     #connect the drone with tello library

    drone.send_rc_control(
        left_right_velocity=0,
        forward_backward_velocity=0,
        up_down_velocity=0,
        yaw_velocity=0)

    print(drone.get_battery())
    drone.streamoff()
    drone.streamon()  # need this to capture the frame
    return drone

def TrackFace(drone,info,img):

    if info[1] != 0:
        cv2.line(img, (int(img.shape[1]*0.5),int(img.shape[0]*0.5)), (int(info[0][0]),int(info[0][1])), (0, 255, 0), 3) #line hijau
        cv2.circle(img,(int(img.shape[1]*0.5),int(img.shape[0]*0.5)),10,(0,0,255),3) #circle merah di camera drone

        print(f"Found a face")
        # for-backward velocity
        velocity = int((3000 - info[1]) * 0.05)
        velocity = int(np.clip(velocity, -10, 10))

        # yaw velocity
        error = info[0][0] - img.shape[1] // 2  # if error positive (+yaw velocity) and vice versa
        velocity1 = int(0.4 * error)
        velocity1 = int(np.clip(velocity1, -10, 10))

        # up down velocity
        error2 = info[0][1] - img.shape[0] // 2  # img.shape[0] // 2
        velocity2 = int(0.4 * error2)
        velocity2 = int(np.clip(velocity2, -10, 10))
    else:
        print(f"Drone is searching for a face")
        velocity = 0
        velocity1 = 20  # rotate in 50mm/s
        velocity2 = 0

    # eksekusi
    if drone.send_rc_control:
        drone.send_rc_control(
            left_right_velocity = 0,
            forward_backward_velocity = velocity,
            up_down_velocity = velocity2,
            yaw_velocity = velocity1
        )

    return velocity,velocity1,velocity2

