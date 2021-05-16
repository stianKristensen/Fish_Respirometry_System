#!/usr/bin/env python
"""
Main Control Node
"""
import rospy
import numpy as np
import os




if __name__ == '__main__':
    try:
        # Init ROS node
        rospy.init_node('mainController', anonymous=True)

        
        # Start Synchronous ROS node execution
        rate = rospy.Rate(10)
        
        
        testValue = 0

        # Control Loop
        while not rospy.is_shutdown():

            testValue = testValue + 1


            # Sleep remaining time
            rate.sleep()


    except rospy.ROSInterruptException:
        pass

