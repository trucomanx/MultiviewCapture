#!/usr/bin/python


import sys
sys.path.append('../lib')


import extras as lib
import FramesAnalizer as FA

import cv2

Show=False;
MaxNumOfImages=10;
############################################################################


Sources, vids, blocks, frame, ret=lib.GetVideoDataAll(start_source=0,end_source=9);
count=0;



while(True):
    state=False;
    for ID in range(len(vids)):
        if vids[ID].isOpened():
            ret[ID], frame[ID] = vids[ID].read();
            cv2.imshow('frame'+str(Sources[ID]), frame[ID]);
            if(blocks[ID].AnalyzeNewFrame(frame[ID],Umbral=25)):
                state=True;
        else:
            exit();
            
    for ID in range(len(vids)):
        if vids[ID].isOpened():
            if(state==True):
                img_name=lib.SaveFrame(frame[ID],count,ID);
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
