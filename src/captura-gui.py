#!/usr/bin/python

import sys
import LibOpenCV as cvextra

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gi.repository import GObject
GObject.threads_init()

from threading     import Thread

class MyWindow(Gtk.Window):
    
    def __init__(self, Umbral=25):
        super().__init__(title="Hello World")
        self.set_border_width(10)
        
        self.cvobj=cvextra.OpenCvClass(count=0,MaxNumOfImages=10,Umbral=25);
        
        # box
        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(mainBox)
        
        # label numimg spinner
        self.label_numimg_spinner = Gtk.Label();
        self.label_numimg_spinner.set_text("Max number of images:");
        mainBox.pack_start(self.label_numimg_spinner, True, True, 0);
        
        # numimg spinner
        adjustment = Gtk.Adjustment(value=10000,
                                    lower=0,
                                    upper=50000,
                                    step_increment=1,
                                    page_increment=5,
                                    page_size=0)
        self.numimg_spinner = Gtk.SpinButton(adjustment=adjustment);
        self.numimg_spinner.connect("value-changed", self.on_numimg_spinbutton_changed)
        mainBox.pack_start(self.numimg_spinner, True, True, 0)
        
        # label spinner
        self.label_spinner = Gtk.Label();
        self.label_spinner.set_text("threshold:");
        mainBox.pack_start(self.label_spinner, True, True, 0);
        
        # spinner
        adjustment = Gtk.Adjustment(value=Umbral,
                                    lower=0,
                                    upper=255,
                                    step_increment=1,
                                    page_increment=5,
                                    page_size=0)
        self.spinner = Gtk.SpinButton(adjustment=adjustment);
        self.spinner.connect("value-changed", self.on_spinbutton_changed)
        mainBox.pack_start(self.spinner, True, True, 0)
        
        # button
        self.button = Gtk.Button(label="Start")
        self.button_state=False;
        self.button.connect("clicked", self.on_button_clicked)
        mainBox.pack_start(self.button, True, True, 0)
        #self.add(self.button)
        
        #getting data
        self.cvobj.MaxNumOfImages=self.numimg_spinner.get_value_as_int();
        self.cvobj.Umbral=self.spinner.get_value_as_int();
        
        
        self.create_new_thread();
        
    def function_temporal(self):
        self.cvobj.start_opencv();
        
        print("function_temporal()","self.reset_the_button()")
        self.reset_the_button();
        
        print("self.create_new_thread()")
        self.create_new_thread();
        print("thread created")
        
        
        
    def create_new_thread(self):
        self.gi_thread = Thread(target=self.function_temporal, args=())
        self.gi_thread.daemon = True;
        
    def reset_the_button(self):
        print("Reseting the button");
        self.button_state=False;
        
        self.cvobj.stop_opencv();
        print("Button reseted");
        
    def on_numimg_spinbutton_changed(self, widget):
        self.cvobj.MaxNumOfImages=self.numimg_spinner.get_value_as_int();
        print("SpinButton numimg changed to",self.cvobj.MaxNumOfImages);
    
    def on_spinbutton_changed(self, widget):
        self.cvobj.Umbral=self.spinner.get_value_as_int();
        print("SpinButton threshold changed to",self.cvobj.Umbral);
        
    def on_button_clicked(self, widget):
        if(self.button_state==False):
            print("Starting the proccess");
            if self.cvobj.count==self.cvobj.MaxNumOfImages:
                self.cvobj.count=0;
            self.button.set_label('Stop');
            #
            self.cvobj.MaxNumOfImages=self.numimg_spinner.get_value_as_int();
            self.cvobj.Umbral=self.spinner.get_value_as_int();
            
            self.button_state=True;
            self.gi_thread.start();# self.function_temporal();
            print("on_button_clicked() started");
            
        else:
            self.reset_the_button();
            self.button.set_label("Start");
            self.create_new_thread();
            #sys.exit()

win = MyWindow(Umbral=25);
win.connect("destroy", Gtk.main_quit);
win.show_all()
Gtk.main()

################################################################################



