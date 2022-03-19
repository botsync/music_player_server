#!/usr/bin/env python

from time import sleep
from std_msgs.msg import String
import time
import os
import rospy
import sys
import random

print(sys.argv)


class StateSwitch:

    def __init__(self):

        self.state_list = ["NAVIGATION", "NAVFORWARD", "NAVRIGHT", "NAVLEFT",  "DOCK", "IDLE", "UNDOCK", "OBSTACLE", "WAIT_FOR_USER_INPUT",
                           "CHARGING", "LOWBATTERY", "INITIALISING", "PAUSE",  "ERROR", "FAULT", "ESTOP", "STO", "TELEOP", "MAPPING", "AUTO", "NOSAFETY"]

        self.state_pub = rospy.Publisher('robot_state', String, queue_size=1)

    # def switch_states(time_duration):


if __name__ == "__main__":

    rospy.init_node('state_switch_node', anonymous=False)

    state_switch_ = StateSwitch()

    sz_ = len(state_switch_.state_list)

    rate = rospy.Rate(0.05)

    while not rospy.is_shutdown():

        rand_idx_ = random.randint(0, sz_ - 1)

        curr_state_ = state_switch_.state_list[rand_idx_]

        state_switch_.state_pub.publish(curr_state_)

        rate.sleep()
