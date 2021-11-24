# Capstone 2021: Vlogging MicroDrone
# Control module

from djitellopy import Tello
import cv2
import numpy as np
import time

#initial condition
pid_fb = [1,1.6,0]
pid_yaw = [0.2,0.5,0]
pid_ud = [0.4,2,0]
error = [0,0,0] #fb,yaw,ud
p_error = [0,0,0] #fb, yaw, ud

def connectingTello():

    drone = Tello()     #defined that drone is tello
    drone.connect()     #connect the drone with tello library

    drone.send_rc_control(
        left_right_velocity=0,
        forward_backward_velocity=0,
        up_down_velocity=0,
        yaw_velocity=0)

    print(drone.get_battery())
    drone.streamon()  # need this to capture the frame
    return drone

def hoverTello(drone):
    time.sleep(5) #wait for 5 seconds before takeoff
    drone.takeoff()
    time.sleep(3) #wait for 3 seconds before go up

    #hover to height 160 cm
    drone_height = drone.get_height()
    drone.move_up(int(160-drone_height))


def TrackFace(drone,info,img):

    if info[1] != 0:
        cv2.line(img, (int(img.shape[1]*0.5),int(img.shape[0]*0.5)), (int(info[0][0]),int(info[0][1])), (0, 255, 0), 3) #line hijau
        cv2.circle(img,(int(img.shape[1]*0.5),int(img.shape[0]*0.5)),10,(0,0,255),3) #circle merah di camera drone

        print(f"Found a face")
        # for-backward velocity
        error[0] = int(15000-info[1])
        velocity = int(pid_fb[0]*error[0] + pid_fb[1]*(error[0]-p_error[0]) + pid_fb[2]*(error[0]+p_error[0]))
        velocity = int(np.clip(velocity,-20,20))
        p_error[0] = error[0]

        # yaw velocity
        error[1] = int(info[0][0]-img.shape[1]//2)
        velocity1 = int(pid_yaw[0] * error[1] + pid_yaw[1] * (error[1] - p_error[1]) + pid_yaw[2] * (error[1] + p_error[1]))
        velocity1 = int(np.clip(velocity1, -20, 20))
        p_error[1] = error[1]

        # up down velocity
        error[2] = int(info[0][1] - img.shape[0] // 2)
        velocity2 = int(pid_ud[0] * error[2] + pid_ud[1] * (error[2] - p_error[2]) + pid_ud[2] * (error[2] + p_error[2]))
        velocity2 = int(np.clip(velocity2, -20, 20))
        p_error[2] = error[2]
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

