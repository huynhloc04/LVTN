#!/usr/bin/env python3

import  sys
sys.path.append('/home/jetson/Documents/LVTN/vision_ws/src/object_detect_pkg/src')

import rospy
from core import detect
from lvtn_pkg.msg import Coordinates

def talker():
    pub = rospy.Publisher("bboxes", Coordinates, queue_size=10)
    rospy.init_node("object_detection", anonymous=True)
    msg = Coordinates()
    # rate = rospy.Rate(14)
    while not rospy.is_shutdown():
        msg.x = 512
        msg.y = 469
        msg.d = 15.5
        pub.publish(msg)
        # rate.sleep()

if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
# {
#     "python.linting.pylintArgs": ["--init-hook",
#         "import sys; sys.path.append('/home/jetson/Documents/LVTN/vision_ws/src/object_detect_pkg')"]
# }