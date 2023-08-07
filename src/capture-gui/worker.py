# worker.py

import sys
sys.path.append('../lib')

from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
#import time

import LibOpenCV as cvextra

class Worker(QObject):
    finished = pyqtSignal()
    ProgressStep = pyqtSignal(int)

    def __init__(self,Nel,Umbral):
        super(Worker, self).__init__();
        self.cvobj=cvextra.OpenCvClass( count=0,
                                        MaxNumOfImages=Nel,
                                        Umbral=Umbral);
    
    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        self.cvobj.start_opencv();
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
    
    def setMaxNumOfImages(self,Nel):
        self.cvobj.MaxNumOfImages=Nel;
        
    def getMaxNumOfImages(self):
        return self.cvobj.MaxNumOfImages;
        
    def setUmbral(self,Umbral):
        self.cvobj.Umbral=Umbral;
        
    def getUmbral(self):
        return self.cvobj.Umbral;
