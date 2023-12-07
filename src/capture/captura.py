#!/usr/bin/python


import sys
sys.path.append('../lib')


import extras as lib
import FramesAnalizer as FA

import cv2

MaxNumOfImages=1000;
start_source=1;
end_source=9;
Umbral=33;
output_dir='/media/fernando/INFORMATION/TMP'

############################################################################


Sources, vids, blocks, frame, ret=lib.GetVideoDataAll(start_source=start_source,end_source=end_source);
count=0;



while(True):
    state=False;
    for ID in range(len(vids)):
        if vids[ID].isOpened():
            
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
