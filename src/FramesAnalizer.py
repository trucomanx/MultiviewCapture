import numpy as np
import cv2
import time

################################################################################
def face_detector_mediapipe():
    import mediapipe as mp
    mp_face_detection = mp.solutions.face_detection
    face_detection=mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5);
    return face_detection;
    
def face_extrator_mediapipe(face_detection,frame0):
    import mediapipe as mp
    results = face_detection.process(cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB))
    if results.detections:
        for detection in results.detections:
            #print("detection",detection)
            height,width,dim=frame0.shape;
            x0=int(detection.location_data.relative_bounding_box.xmin*width);
            x0=max(x0, 0);x0=min(x0, frame0.shape[1]);
            y0=int(detection.location_data.relative_bounding_box.ymin*height);
            y0=max(y0, 0);x0=min(y0, frame0.shape[0]);
            dx=int(detection.location_data.relative_bounding_box.width*width);
            dy=int(detection.location_data.relative_bounding_box.height*height);
            frame0=frame0[y0:(y0+dy), x0:(x0+dx)];
            frame0 = cv2.resize(frame0, (100,100), interpolation = cv2.INTER_AREA)
            #cv2.imwrite('face' + str(time.time_ns()) + '.png', frame0)
            break;
    return frame0;
################################################################################
def face_detector_retinaface():
    from retinaface.pre_trained_models import get_model
    model = get_model("resnet50_2020-07-20", max_size=2048);
    model.eval();
    return model;

def face_extrator_retinaface(model,frame0):
    annotation = model.predict_jsons(frame0)
    if len(annotation)>0:
        x_min, y_min, x_max, y_max = annotation[0]['bbox']
        #cv2.imwrite("face"+str(time.time_ns())+".png", frame0);
        print(frame0.shape)
        print(int(x_min), int(y_min), int(x_max), int(y_max))
        frame0=frame0[int(y_min):int(y_max), int(x_min):int(x_max)];
        frame0 = cv2.resize(frame0, (100,100), interpolation = cv2.INTER_AREA)
    return frame0;

################################################################################

def face_detector_opencv():
    path = cv2.data.haarcascades +'haarcascade_frontalface_default.xml'
    return cv2.CascadeClassifier(path);
    

def face_extrator_opencv(detector,frame0):
    face_rects = detector.detectMultiScale(frame0, scaleFactor=1.3, minNeighbors=5)
    if len(face_rects)>0:
        x,y,w,h = face_rects[0];
        frame0=frame0[y:y+h, x:x+w];
        frame0 = cv2.resize(frame0, (100,100), interpolation = cv2.INTER_AREA)
        #cv2.imwrite("face"+str(time.time_ns())+".png", frame0);
    return frame0;

################################################################################
   
class FramesAnalizer:

    def __init__(self):
        self.frame1 = np.zeros((0, 0, 0));
        
        ##############################################
        self.face_detector=face_detector_mediapipe();
        #self.face_detector=face_detector_opencv();
        #self.face_detector=face_detector_retinaface();
        ##############################################
    
    def AnalyzeNewFrame(self,frame0,Umbral):
        ##############################################
        frame0=face_extrator_mediapipe(self.face_detector,frame0);
        ##frame0=face_extrator_opencv(self.face_detector,frame0);
        #frame0=face_extrator_retinaface(self.face_detector,frame0);
        ##############################################
         
        if   (np.sum(self.frame1.shape) == 0) and (frame0.shape!=0) :
            #print("if1")
            self.frame1=frame0;
            return True;
        elif (np.sum(self.frame1.shape) != 0) and (frame0.shape!=0) :
            #print("if2")
            if frame0.shape == self.frame1.shape:
                #print("if2-shape igual")
                
                frame_diff = cv2.absdiff(frame0,self.frame1);
                disp_frame = np.uint8(255.0*frame_diff/float(frame_diff.max()))
                umbral=disp_frame.mean();
                #cv2.imwrite("face"+str(time.time_ns())+"-equ.png", frame0);
                #print("Umbral:",umbral)
                if umbral>Umbral:
                    self.frame1=frame0;
                    return True;
                else:
                    return False;
                
            else:
                #print("if2-shape different")
                #cv2.imwrite("face"+str(time.time_ns())+"-dif.png", frame0);
                self.frame1=frame0;
                return True;
        else:
            #print("else")
            return False;
        return False;
