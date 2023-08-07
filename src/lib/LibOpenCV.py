#!/usr/bin/python

import os
import sys
import extras as lib
import FramesAnalizer as FA

import cv2

############################################################################
class OpenCvClass:
    def __init__(self,count=0,MaxNumOfImages=10,Umbral=25,Directory='./'):
        self.MaxNumOfImages = MaxNumOfImages;
        self.count = count;
        self.loop = False;
        self.Umbral= Umbral;
        self.Directory = Directory;
    
    def stop_opencv(self):
        self.loop = False;
    
    def start_opencv(self, start_source=0,end_source=9,imshow=False):
        Sources, vids, blocks, frame, ret = lib.GetVideoDataAll(start_source=start_source,end_source=end_source);
        self.loop = True;
        
        while(self.loop):
            #print("passsei",self.count)
            state=False;
            for ID in range(len(vids)):
                if vids[ID].isOpened():
                    ret[ID], frame[ID] = vids[ID].read();
                    if imshow:
                        cv2.imshow('frame'+str(Sources[ID]), frame[ID]);
                    if(blocks[ID].AnalyzeNewFrame(frame[ID],Umbral=self.Umbral)):
                        state=True;
                else:
                    self.loop=False;
            
            for ID in range(len(vids)):
                if vids[ID].isOpened():
                    if(state==True):
                        img_name=lib.SaveFrame(frame[ID],self.count+1,ID,Directory=self.Directory);
                        print("Image",img_name,"saved")
                else:
                    self.loop=False;
            
            if(state==True):
                self.count=self.count+1;
            
            # the 'q' button for quit
            if imshow:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.loop=False;
            
            if self.count>=self.MaxNumOfImages:
                print("Obtained",self.count,"images.")
                self.loop=False;
        print("Ended start_opencv();");
