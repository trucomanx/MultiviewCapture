
import os
import cv2


def GetSources(init=0,end=9):
    Sources=[];
    for source in range(init,end+1):
        #print(source)
        cap = cv2.VideoCapture(source) 
        if cap is None or not cap.isOpened():
            #print('Error opening source',source);
            pass
        else:
            Sources.append(source);
        cap.release();
    return Sources;
    
def GetVideoIDs(Sources):
    vids=[];
    for source in Sources:
        # define a video capture object
        vids.append(cv2.VideoCapture(source));
    return vids;

import FramesAnalizer as FA
def GetVideoDataAll(start_source=0,end_source=9):
    Sources=GetSources(start_source,end_source);
    vids=[];
    blocks = [];
    frame  = [];
    ret  = [];
    if len(Sources)==0:
        print("No sources found");
        exit();
    for source in Sources:
        # define a video capture object
        vids.append(cv2.VideoCapture(source));
        blocks.append(FA.FramesAnalizer());
        frame.append(None);
        ret.append(None);
    return Sources, vids, blocks, frame, ret;
    
def SaveFrame(frame,count,ID,Directory='./'):
    img_name = os.path.join(Directory,"frame_count"+str(count)+"_cam"+str(ID)+".png");
    
    cv2.imwrite(img_name, frame);
    return img_name;    
