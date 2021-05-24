#!/usr/bin/env python
# license removed for brevity
# import rospy
# from fish_respirometry_system.msg import menuData
import tkinter as tk
from tkinter.constants import END, LEFT, RIGHT

import configparser

import os

# def talker():
#     pub = rospy.Publisher('chatter', String, queue_size=10)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#     while not rospy.is_shutdown():
#         hello_str = "hello world %s" % rospy.get_time()
#         rospy.loginfo(hello_str)
#         pub.publish(hello_str)
#         rate.sleep()


# -----CONFIG FILE-----
config = configparser.ConfigParser()

if os.path.exists('config.ini') == False:
    config['Procedure Settings'] = {
        'start_flow_velocity_[cm/s]': '0.5',
        'end_flow_velocity_[cm/s]': '20',
        'flow_velocity_stepsize_[cm/s]': '0.5',
        'test_time_[min]': '20',
        'flush_time_[min]': '10',
        'flush_pump_strength_[0-255]': '100'
        }

    config['Maintenance'] = {
        'fill_time_[min]': '2',
        'flush_time_[min]': '5',
        'clean_time_[min]': '15',
        'drain_time_[min]': '3',
        'pump_strength_[0-255]': '100'
        }
    
    config['System Values'] = {
        'min_flow_velocity_[cm/s]': '0.5',
        'max_flow_velocity_[cm/s]': '20',
        'total_volume_[ml]': '40.8'
        }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read('config.ini')



def test_settings():
    testSettingsWindow = tk.Tk()

    # Start flow velocity
    label_startFlow = tk.Label(master=testSettingsWindow, text="Starting Flow Velocity [cm/s]")
    label_startFlow.grid(row=0, column=0)
    entry_startFlow = tk.Entry(master=testSettingsWindow, width=5, exportselection=0)
    entry_startFlow.insert(END, config['Procedure Settings']['start_flow_velocity_[cm/s]'])
    entry_startFlow.grid(row=0, column=1)

    # End flow velocity
    label_endFlow = tk.Label(master=testSettingsWindow, text="End Flow Velocity [cm/s]")
    label_endFlow.grid(row=1, column=0)
    entry_endFlow = tk.Entry(master=testSettingsWindow, width=5, exportselection=0)
    entry_endFlow.insert(END, config['Procedure Settings']['end_flow_velocity_[cm/s]'])
    entry_endFlow.grid(row=1, column=1)

        
    # Update config upon pressing the "SAVE" button
    button_saveStartFlow = tk.Button(master=testSettingsWindow, text ="SAVE", command = lambda: save_procedureSettings(config, entry_startFlow.get(), entry_endFlow.get()))
    button_saveStartFlow.grid(column=1)


    testSettingsWindow.mainloop()

# Update procedure settings values when called
def save_procedureSettings(config, startFlow, endFlow):
    config['Procedure Settings'] = {
    'start_flow_velocity_[cm/s]': startFlow,
    'end_flow_velocity_[cm/s]': endFlow,
    'flow_velocity_stepsize_[cm/s]': '0.5',
    'test_time_[min]': '20',
    'flush_time_[min]': '10',
    'flush_pump_strength_[0-255]': '100'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print('CONFIG VALUES UPDATED')



window = tk.Tk()


frame_a = tk.Frame()
label_a = tk.Label(master=frame_a, text="I'm in Frame A")
label_a.pack()


frame_b = tk.Frame()
label_b = tk.Label(master=frame_b, text="I'm in Frame B")
label_b.pack()
testSettingsButton = tk.Button(master=frame_b, text ="Test Settings", command = test_settings)
testSettingsButton.pack()

# Swap the order of `frame_a` and `frame_b`
frame_a.pack()
frame_b.pack()


window.mainloop()

# if __name__ == '__main__':
#     try:
#         # Initialize nodes
#         rospy.init_node('interface')
        
#         while not rospy.is_shutdown():
            
#     except rospy.ROSInterruptException:
#         pass
