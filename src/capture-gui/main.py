# main.py
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QDir

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFrame

import sys
import time
import worker


class Form(QWidget):

    def __init__(self):
        super().__init__()
        
        # window
        self.setGeometry(0,0,300,200);# width height
        self.setWindowTitle("Camera-Gui")

        #label_numofimg
        self.label_outdir=QLabel("Select the output directory:");
        #lineedit_outdir
        self.lineedit_outdir=QLineEdit(QDir.homePath()); 
        #pushbutton_outdir
        self.pushbutton_outdir=QPushButton("Select");
        self.pushbutton_outdir.clicked.connect(self.on_select_outputdir)
        #label_sources
        self.label_sources=QLabel("Sources 0 until :");
        #spin_end
        self.spin_endsource=QSpinBox();
        self.spin_endsource.setRange(0,10);
        self.spin_endsource.setValue(3);
        self.spin_endsource.valueChanged.connect(self.on_spin_endsource_changed);
        #separatorline
        self.separatorLine1 = QFrame()
        self.separatorLine1.setFrameShape( QFrame.HLine )
        self.separatorLine1.setFrameShadow( QFrame.Raised )
        #label_numofimg
        self.label_numofimg=QLabel("Max number of images:");
        #spin_numofimg
        self.spin_numofimg=QSpinBox();
        self.spin_numofimg.setRange(0,100000);
        self.spin_numofimg.setValue(15);
        self.spin_numofimg.valueChanged.connect(self.on_spin_numofimg_changed);
        #label_threshold
        self.label_threshold=QLabel("Threshold:");
        #spin_threshold
        self.spin_threshold=QSpinBox();
        self.spin_threshold.setRange(0,255);
        self.spin_threshold.setValue(25);
        self.spin_threshold.valueChanged.connect(self.on_spin_threshold_changed);
        #pushbutton
        self.pushbutton=QPushButton("Start");
        self.pushbutton.clicked.connect(self.on_button_clicked)
        #rogress bar
        self.progress_bar = QProgressBar();
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0,self.spin_numofimg.value());

        #HBox1
        self.hbox1 = QHBoxLayout();
        self.hbox1.addWidget(self.lineedit_outdir)
        self.hbox1.addWidget(self.pushbutton_outdir)

        #VBox
        self.vbox=QVBoxLayout();
        self.vbox.addWidget(self.label_outdir)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addWidget(self.label_sources)
        self.vbox.addWidget(self.spin_endsource)
        self.vbox.addWidget(self.separatorLine1)
        self.vbox.addWidget(self.label_numofimg)
        self.vbox.addWidget(self.spin_numofimg)
        self.vbox.addWidget(self.label_threshold)
        self.vbox.addWidget(self.spin_threshold)
        self.vbox.addWidget(self.pushbutton)
        self.vbox.addWidget(self.progress_bar)

        #
        self.setLayout(self.vbox)

        #################################################

        # 1 - create Worker and Thread inside the Form
        self.obj_worker = worker.Worker(self.spin_numofimg.value(),
                                        self.spin_threshold.value(),
                                        self.lineedit_outdir.text()
                                        );  # no parent!
        self.thread = QThread()  # no parent!

        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.obj_worker.ProgressStep.connect(self.onProgressStep)

        # 3 - Move the Worker object to the Thread object
        self.obj_worker.moveToThread(self.thread)

        # 4 - Connect Worker Signals to the Thread slots
        self.obj_worker.finished.connect(self.onProgressComplete)

        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.obj_worker.procCounter)

        # 7 - Start the form
        self.initUI()
        
    #################################################
    def on_select_outputdir(self):
        folderpath = QFileDialog.getExistingDirectory(self,'Select Folder')
        self.lineedit_outdir.setText(folderpath);
        self.obj_worker.setOutputDir(folderpath);
    #################################################

    def initUI(self):
        self.move(300, 150)
        self.show()
    
    ##################################
    def on_spin_endsource_changed(self):
        self.obj_worker.setEndSource(self.spin_endsource.value());
        print("SpinButton endsource changed to",self.obj_worker.getEndSource());
    
    ##################################
    def on_spin_numofimg_changed(self):
        self.obj_worker.setMaxNumOfImages(self.spin_numofimg.value());
        self.progress_bar.setRange(0,self.spin_numofimg.value());
        print("SpinButton numimg changed to",self.obj_worker.getMaxNumOfImages());


    def on_spin_threshold_changed(self):
        self.obj_worker.setUmbral(self.spin_threshold.value());
        print("SpinButton threshold changed to",self.obj_worker.getUmbral());
        
    #################################################
    
    def onProgressStep(self, i):
        self.progress_bar.setValue(i)
        
    def onProgressComplete(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("This work was complete")
        msg.setInformativeText("Press OK to return to program");
        msg.setWindowTitle("Attention")
        msg.setDetailedText("The take of pictures was finalized. Was taken "+
                            str(self.obj_worker.getMaxNumOfImages())+
                            " pictures by camera.");
        msg.setStandardButtons(QMessageBox.Ok);
        msg.exec_();
        
        self.reset_work();
        
    def reset_work(self):
        self.thread.exit(0);
        
        self.progress_bar.setValue(0)
        self.pushbutton.setText("Start");
        self.pushbutton.setEnabled(True);
    
    #################################################
    def on_button_clicked(self):
            
        # Start the thread
        self.thread.start()
        self.pushbutton.setText("Stop");
        self.pushbutton.setEnabled(False);
        


app = QApplication(sys.argv)

form = Form()

sys.exit(app.exec_())
