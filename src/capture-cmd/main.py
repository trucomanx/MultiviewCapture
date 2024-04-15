#!/usr/bin/python


import sys
sys.path.append('../lib')


import extras as lib
import FramesAnalizer as FA

import cv2

MaxNumOfImages=15;
start_source=1;
end_source=9;
Umbral=3000;
output_dir='/media/fernando/INFORMATION/TMP'

############################################################################


Sources, vids, blocks, frame, ret=lib.GetVideoDataAll(start_source=start_source,end_source=end_source);
count=0;



while(True):
    state=False;
    for ID in range(len(vids)):
        if vids[ID].isOpened():
            #1280x720,960x540 #1024x576
            #vids[ID].set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            #vids[ID].set(cv2.CAP_PROP_FRAME_HEIGHT,720)
            vids[ID].set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
            ret[ID], frame[ID] = vids[ID].read();
            if ret[ID]:
                cv2.imshow('frame'+str(Sources[ID]), frame[ID]);
                if(blocks[ID].AnalyzeNewFrame(frame[ID],Umbral=Umbral)):
                    state=True;
        else:
            exit();
            
    for ID in range(len(vids)):
        if vids[ID].isOpened():
            if  (state==True) and ret[ID]:
                img_name=lib.SaveFrame(frame[ID],count,ID,Directory=output_dir);
                print("Image",img_name,"saved")
        else:
            exit();
    
    if(state==True):
        count=count+1;

    # the 'q' button for quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if count>MaxNumOfImages:
        exit();
