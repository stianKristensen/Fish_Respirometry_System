#!/usr/bin/env python
# license removed for brevity
import rospy
#from interfaceData.msg import blabla
import configparser



# Operation functions

# Miscellaneous functions
def increment(value): # increments the first value of an array
    value[0] += 1
    return value[0]

# State Machine and data handling
class RespSystem(config):
    def __init__(self):
        # Read values from configuration file
        maintenance = config['Maintenance']
        self.flush_time = maintenance['flush_time_[min]']
        self.clean_time = maintenance['clean_time_[min]']
        self.drain_time = maintenance['drain_time_[min]']
        self.maintenance_pump_PWM = maintenance['pump_strength_[0-255]']

        systemValues = config['System Values']
        self.min_flow_velocity = systemValues['min_flow_velocity_[cm/s]']
        self.max_flow_velocity = systemValues['max_flow_velocity_[cm/s]']
        self.total_volume = systemValues['total_volume_[ml]']

        # Initiate system variables
        self.inletPumpPWM = 0
        self.inletPumpDirection = 1 # 0 drains while 1 fills the system

        self.outletPumpPWM = 0
        self.outletPumpDirection = 0 # 0 drains while 1 fills the system

        self.impellerRPM = 0

        b = [0] #Counter used to assign unique values to states

        # states
        self.state_idle = increment(b) # idle mode of the system
        self.state_stop = increment(b) # fully stops the system

        # initial state
        self.state = self.state_idle

    def drain(self):
        self.inletPumpPWM = self.maintenance_pump_PWM
        self.inletPumpDirection = 0

        self.outletPumpPWM = self.maintenance_pump_PWM
        self.outletPumpDirection = 0

        self.impellerRPM = 0

if __name__ == '__main__':
        # Tries to initialize node if roscore is properly running
    try:
        # Initialize ROS node
        rospy.init_node('operationControl', anonymous=True)

        # Read config.ini file
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Initialize system
        respSystem = RespSystem(config)

        # Start Synchronous ROS node execution
        rate = rospy.Rate(10) # Hz

        while not rospy.is_shutdown():
            #Loop code

            # Sleep remaining time
            rate.sleep()
            
    except rospy.ROSInterruptException:
        pass