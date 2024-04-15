#!/usr/bin/python


import sys
sys.path.append('../lib')


import extras as lib
import FramesAnalizer as FA

import cv2

start_source=1;
end_source=10;
brightness=128;

############################################################################


Sources, vids, blocks, frame, ret=lib.GetVideoDataAll(start_source=start_source,end_source=end_source);


while(True):
    for ID in range(len(vids)):
        if vids[ID].isOpened():
            #1280x720,960x540 #1024x576
            #vids[ID].set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            #vids[ID].set(cv2.CAP_PROP_FRAME_HEIGHT,720)
            vids[ID].set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
            vids[ID].set(cv2.CAP_PROP_BRIGHTNESS,brightness)
            #print(vids[ID].get(cv2.CAP_PROP_BRIGHTNESS))
            
            ret[ID], frame[ID] = vids[ID].read();
            if ret[ID]:
                cv2.imshow('frame'+str(Sources[ID]), frame[ID]);
        else:
            exit();
            
    # the '+' button
    KEY=cv2.waitKey(1) & 0xFF;
    
    if  KEY == ord('p'):
        brightness=brightness+2;
        print("brightness:",brightness);
    # the '-' button
    if  KEY == ord('m'):
        brightness=brightness-2;
        print("brightness:",brightness);
        
    # the 'q' button for quit
    if  KEY == ord('q'):
        break
    
