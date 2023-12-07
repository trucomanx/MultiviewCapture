# worker.py

import sys
sys.path.append('../lib')

from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
#import time

import LibOpenCV as cvextra

class Worker(QObject):
    finished = pyqtSignal()
    ProgressStep = pyqtSignal(int)

    def __init__(self,Nel,Umbral,Directory,start_source=0,end_source=9):
        super(Worker, self).__init__();
        self.cvobj=cvextra.OpenCvClass( count=0,
                                        MaxNumOfImages=Nel,
                                        Umbral=Umbral,
                                        Directory=Directory);
        self.start_source = start_source;
        self.end_source   = end_source;

    
    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        # busca cameras de 0 a 9
        self.cvobj.start_opencv(start_source=self.start_source,end_source=self.end_source,imshow=False);
        count=0;
        while True:
            if self.cvobj.count>count:
                count=self.cvobj.count;
            self.ProgressStep.emit(count);
            
            print('\nself.cvobj.count:',self.cvobj.count)
            print(' ')
            
            if self.cvobj.count>=self.cvobj.MaxNumOfImages:
                break;

        self.stop_opencv();
        self.finished.emit();
    
    def stop_opencv(self):
        self.cvobj.stop_opencv();
        self.cvobj.count=0;
        print("self.cvobj.stop_opencv()");
    
    def setStartSource(self,Nel):
        self.start_source=Nel;
        
    def getStartSource(self):
        return self.start_source;
        
    def setEndSource(self,Nel):
        self.end_source=Nel;
        
    def getEndSource(self):
        return self.end_source;
    
    def setMaxNumOfImages(self,Nel):
        self.cvobj.MaxNumOfImages=Nel;
        
    def getMaxNumOfImages(self):
        return self.cvobj.MaxNumOfImages;
        
    def setOutputDir(self,Directory):
        self.cvobj.Directory=Directory;
        
    def getOutputDir(self):
        return self.cvobj.Directory;
        
    def setUmbral(self,Umbral):
        self.cvobj.Umbral=Umbral;
        
    def getUmbral(self):
        return self.cvobj.Umbral;
