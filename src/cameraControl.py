#!/usr/bin/env python
# license removed for brevity
import rospy
import cv2
import numpy as py
import os
#from fish_respirometry_system.msg import menuData

def focusing(val):
	value = (val << 4) & 0x3ff0
	data1 = (value >> 8) & 0x3f
	data2 = value & 0xf0
	os.system("i2cset -y 6 0x0c %d %d" % (data1,data2))
	
def sobel(img):
	img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	img_sobel = cv2.Sobel(img_gray,cv2.CV_16U,1,1)
	return cv2.mean(img_sobel)[0]

def laplacian(img):
	img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	img_sobel = cv2.Laplacian(img_gray,cv2.CV_16U)
	return cv2.mean(img_sobel)[0]


# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps 
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

def gstreamer_pipeline (capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=60, flip_method=0) :   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))

def show_camera():
    max_index = 10
    max_value = 0.0
    last_value = 0.0
    dec_count = 0
    focal_distance = 10
    focus_finished = False
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print gstreamer_pipeline(flip_method=0)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        window_handle = cv2.namedWindow('CSI Camera', cv2.WINDOW_AUTOSIZE)
        # Window 
        while cv2.getWindowProperty('CSI Camera',0) >= 0:
            ret_val, img = cap.read()
            cv2.imshow('CSI Camera',img)
            
            if dec_count < 6 and focal_distance < 1000:
                #Adjust focus
                focusing(focal_distance)
                #Take image and calculate image clarity
                val = laplacian(img)
                #Find the maximum image clarity
                if val > max_value:
                    max_index = focal_distance
                    max_value = val
                    
                #If the image clarity starts to decrease
                if val < last_value:
                    dec_count += 1
                else:
                    dec_count = 0
                #Image clarity is reduced by six consecutive frames
                if dec_count < 6:
                    last_value = val
                    #Increase the focal distance
                    focal_distance += 10

            elif not focus_finished:
                #Adjust focus to the best
                focusing(max_index)
                focus_finished = True
            # This also acts as 
            keyCode = cv2.waitKey(16) & 0xff
            # Stop the program on the ESC key
            if keyCode == 27:
                break
            elif keyCode == 10:
                max_index = 10
                max_value = 0.0
                last_value = 0.0
                dec_count = 0
                focal_distance = 10
                focus_finished = False
        cap.release()
        cv2.destroyAllWindows()
    else:
        print 'Unable to open camera'

if __name__ == '__main__':
    try:
        show_camera()
    except rospy.ROSInterruptException:
        pass