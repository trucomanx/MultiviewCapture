#!/usr/bin/python


import sys
import extras as lib
import FramesAnalizer as FA

import cv2

Show=False;
MaxNumOfImages=10;
############################################################################


Sources=lib.GetSources(0,9);
vids=lib.GetVideoIDs(Sources);

vids=[];
blocks = []
for source in Sources:
    # define a video capture object
    vids.append(cv2.VideoCapture(source));
    blocks.append(FA.FramesAnalizer());

count=0;



while(True):
    state=False;
    for ID in range(len(vids)):
        if vids[ID].isOpened():
            ret, frame = vids[ID].read();
            
            cv2.imshow('frame'+str(Sources[ID]), frame);
            if(blocks[ID].AnalyzeNewFrame(frame)):
                lib.SaveFrame(frame,count,ID);
                state=True;
        else:
            exit();
    
    if(state==True):
        count=count+1;

    # the 'q' button for quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if count>MaxNumOfImages:
        exit();
