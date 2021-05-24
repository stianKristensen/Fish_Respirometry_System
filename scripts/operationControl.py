#!/usr/bin/env python
# license removed for brevity
import rospy
#from interfaceData.msg import blabla



# Operation functions

# Miscellaneous functions
def increment(value): # increments the first value of an array
    value[0] += 1
    return value[0]

# State Machine and data handling
class RespSystem():
    def __init__(self):
        # self.leftWheel = leftWheelIdle
        # self.rightWheel = rightWheelIdle
        # self.servoTargets = initialServos[:]
        # self.driveBias = 0 # -1 turn left, 1 turn right, 0 no bias
        # self.drive = False #variable used for timed movement

        b = [0] #Counter used to assign unique values to states

        # states
        self.state_idle = increment(b) # idle mode of the system
        self.state_stop = increment(b) # fully stops the system

        # initial state
        self.state = self.state_idle

if __name__ == '__main__':
        # Tries to initialize node if roscore is properly running
    try:
        # Initialize ROS node
        rospy.init_node('operationControl', anonymous=True)

        # Read config.ini file
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Initialize system
        respSystem = RespSystem()

        # Start Synchronous ROS node execution
        rate = rospy.Rate(10) # Hz

        while not rospy.is_shutdown():
            #Loop code

            # Sleep remaining time
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass