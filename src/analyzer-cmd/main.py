#!/usr/bin/python
import sys


import os
#os.makedirs('./tmp',exist_ok=True)
os.system('git clone https://github.com/trucomanx/VideoImageTools.git') # Cloning
os.system('git clone https://github.com/trucomanx/OpenPifPafTools.git') # Cloning
os.system('git clone https://github.com/trucomanx/cnn_emotion4.git') # Cloning

sys.path.append('VideoImageTools/src')
sys.path.append('OpenPifPafTools/src')
sys.path.append('cnn_emotion4/library')

sys.path.append('../lib')


import extras as lib
import FrameAnalyzer as FA
import Classifier as mylib

import cv2

start_source=0;
end_source=0;


################################################################################
import openpifpaf
Clf=mylib.Emotion4Classifier('efficientnet_b3');
predictor = openpifpaf.Predictor(checkpoint='shufflenetv2k16')#'shufflenetv2k16-wholebody'
################################################################################


Sources, vids, blocks, frame, ret=lib.GetVideoDataAll(start_source=start_source,end_source=end_source);


while(True):
    for ID in range(len(vids)):
        if vids[ID].isOpened():
            #1280x720,960x540 #1024x576
            #v4l2-ctl -d /dev/video0 --list-formats-ext
            #vids[ID].set(cv2.CAP_PROP_FRAME_WIDTH, 424)
            #vids[ID].set(cv2.CAP_PROP_FRAME_HEIGHT,240)
            #vids[ID].set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
            #print(vids[ID].get(cv2.CAP_PROP_FRAME_WIDTH))
            #print(vids[ID].get(cv2.CAP_PROP_FRAME_HEIGHT))
            vids[ID].set(cv2.CAP_PROP_BRIGHTNESS,150)
            
            ret[ID], frame[ID] = vids[ID].read();
            if ret[ID]:
                frame[ID]=FA.my_func(Clf,predictor,frame[ID]);
                cv2.imshow('frame'+str(Sources[ID]), frame[ID]);
        else:
            exit();
            
    # the 'q' button for quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
