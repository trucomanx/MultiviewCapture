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
    
def SaveFrame(frame,count,ID):
    img_name = "frame_count"+str(count)+"_cam"+str(ID)+".png";
    
    cv2.imwrite(img_name, frame);
    return img_name;    
