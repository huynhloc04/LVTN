#!/usr/bin/env python3

import  sys
sys.path.append('/home/jetson/Documents/LVTN/vision_ws/src/object_detect_pkg/src')

import cv2
import ctypes
import nanocamera as nano
from detectGrape import YoLov5TRT, warmUpThread, findBbox
from stereoVision import findDis
import rospy
from lvtn_pkg.msg import Coordinates

def talker(yolov5_wrapper):
    #   ROS initilization
    pub = rospy.Publisher("bboxes", Coordinates, queue_size=10)
    rospy.init_node("object_detection", anonymous=True)
    msg = Coordinates()

    #   ================== Read video from stereo camera ==================
    camLeft = nano.Camera(device_id=0, flip=4, width=640, height=480)
    camRight = nano.Camera(device_id=1, flip=4, width=640, height=480)
    # rate = rospy.Rate(14)
    while not rospy.is_shutdown():
        frameLeft = camLeft.read()
        frameRight = camRight.read()

        #   Detect grape in 2D space
        bboxesLeft, bboxesRight = findBbox(yolov5_wrapper, frameLeft, frameRight)

        if bboxesLeft.size and bboxesRight.size:
            centerLeft = (int(bboxesLeft[0]) + int(bboxesLeft[2] / 2), int(bboxesLeft[1]) + int(bboxesLeft[3] / 2))
            centerRight = (int(bboxesRight[0]) + int(bboxesRight[2] / 2), int(bboxesRight[1]) + int(bboxesRight[3] / 2))
            #   Distance estimation
            distance = findDis(centerRight, centerLeft, frameRight, frameLeft)

            #   Publishing a message
            msg.x = centerLeft[0]
            msg.y = centerLeft[1]
            msg.d = distance
            pub.publish(msg)
            # rate.sleep()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
    camLeft.release()
    camRight.release()

    del camLeft
    del camRight

if __name__ == "__main__":
    #   Load weights of model
    PLUGIN_LIBRARY = "/home/jetson/Documents/LVTN/vision_ws/src/lvtn_pkg/src/libmyplugins.so"
    engine_file_path = "/home/jetson/Documents/LVTN/vision_ws/src/lvtn_pkg/src/yolov5s.engine"
    ctypes.CDLL(PLUGIN_LIBRARY)
    #   Load labels
    categories = ["grape"]

    yolov5_wrapper = YoLov5TRT(engine_file_path)
    try:
        for i in range(10):
            # Create a new thread to do warm_up
            thread1 = warmUpThread(yolov5_wrapper)
            thread1.start()
            thread1.join()

        #   Call ROS publisher
        talker(yolov5_wrapper)
        
    finally:
        yolov5_wrapper.destroy()
