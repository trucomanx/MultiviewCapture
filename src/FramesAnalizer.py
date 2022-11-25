import numpy as np
import cv2
import time


class FramesAnalizer:

    def __init__(self):
        self.frame1 = np.zeros((0, 0, 0));
        # initialize the HOG descriptor/person detector
        
        path = cv2.data.haarcascades +'haarcascade_frontalface_default.xml'
        self.face_detector = cv2.CascadeClassifier(path)


    
    def AnalyzeNewFrame(self,frame0):
        face_rects = self.face_detector.detectMultiScale(frame0, scaleFactor=1.1, minNeighbors=5)
        if len(face_rects)>0:
            x,y,w,h = face_rects[0];
            frame0=frame0[y:y+h, x:x+w];
            frame0 = cv2.resize(frame0, (100,100), interpolation = cv2.INTER_AREA)
            #cv2.imwrite("face"+str(time.time_ns())+".png", frame0);
         
        if   (np.sum(self.frame1.shape) == 0) and (frame0.shape!=0) :
            self.frame1=frame0;
            return True;
        elif (np.sum(self.frame1.shape) != 0) and (frame0.shape!=0) :
            if frame0.shape == self.frame1.shape:

                
                frame_diff = cv2.absdiff(frame0,self.frame1);
                disp_frame = np.uint8(255.0*frame_diff/float(frame_diff.max()))
                if disp_frame.mean()>100:
                    self.frame1=frame0;
                    return True;
                else:
                    return False;
                
            else:
                self.frame1=frame0;
                return True;
        else:
            return False;
        return True;
