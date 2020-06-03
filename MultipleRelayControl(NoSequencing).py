import os
import time
import threading
import kivy
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
from kivy.app import App   
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.image import AsyncImage
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window
from kivy.uix.widget import Widget 
from kivy.lang import builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, NumericProperty, DictProperty
from kivy.lang import Builder

KV = """
ScreenManager:
    Screen:
        name: 'mainMenu'
        GridLayout:
            cols: 3
            Image: 
                source: 'logo.png'
                size: 180,120
            Label:
                text: 'Main Menu'
                font_size: 28
                bold: True
            Label:
                text: ''
            Label:
                text: ''
            Button:
                text: 'Task Manager'
                font_size: 18
                on_press: root.current = 'taskManager'
            Label:
                text: ''
            Label:
                text: ''
            Button:
                text: 'Task Settings'
                font_size: 18
                on_press: root.current = 'taskSettings'
            Label:
                text: ''
            Label:
                text: ''
            Label:
                text: ''
            Label:
                text: 'Current kivy test version'

    TaskManger:
        name: 'taskManager'
        id: taskManager 
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: 105
                Image: 
                    source: 'logo.png'      
                Label:
                    text: 'Task Manager'
                    font_size: '28'
                    bold: True
                Button:
                    size_hint_x: 0.5
                    text: 'Task Settings'
                    font_size: 16
                    on_press: root.current = 'taskSettings'
                Button:
                    size_hint_x: 0.5 
                    text: 'Main Menu'
                    font_size: 16
                    on_press: root.current = 'mainMenu'
            GridLayout:
                cols: 4
                rows: 1
                GridLayout:
                    cols: 1
                    Label: 
                        text: 'Relay 1' 
                    Label:
                        text: 'Preset: ' + str(app.data[0])
                    Label:
                        text: 'Extend Time: ' + str(app.data[1])
                    Label:
                        text: 'Retract Time: ' + str(app.data[2])
                    Button:
                        text: 'Manual Extend'
                        on_press: taskManager.relay1_manual_extend_retract(self)
                    Label:
                        text: 'Current Cycles: ' + str(taskManager.current_cycles_relay1) 
                    GridLayout:
                        cols: 2
                        row_default_height: 50
                        row_default_width: 50
                        row_force_defaults: True
                        Button:
                            text: 'Pause'
                            on_press: taskManager.relay1_pause(self)
                            background_color:  [1,0,0,1]
                            color: [0,0,0,1]    
                        Button: 
                            text: 'Reset'
                            background_color:  [1,0,0,1]
                            color: [0,0,0,1]
                            on_press: taskManager.relay1_reset(self)
                        Button:
                            text: 'Start'
                            background_color: [0,1,0,1]
                            color: [0,0,0,1]
                            on_press: taskManager.relay1_start(self)

                    GridLayout:
                        cols: 1
                        Label: 
                            text: 'Relay 2' 
                        Label:
                            text: 'Preset: ' + str(app.data[3])
                        Label:
                            text: 'Extend Time: ' + str(app.data[4])
                        Label:
                            text: 'Retract Time: ' + str(app.data[5])
                        Button:
                            text: 'Manual Extend'
                            on_press: taskManager.relay2_manual_extend_retract(self)
                        Label:
                            text: 'Current Cycles: ' + str(taskManager.current_cycles_relay2) 
                        GridLayout:
                            cols: 2
                            row_default_height: 50
                            row_default_width: 50
                            row_force_defaults: True
                            Button:
                                text: 'Pause'
                                on_press: taskManager.relay2_pause(self)
                                background_color:  [1,0,0,1]
                                color: [0,0,0,1]    
                            Button: 
                                text: 'Reset'
                                background_color:  [1,0,0,1]
                                color: [0,0,0,1]
                                on_press: taskManager.relay2_reset(self)
                            Button:
                                text: 'Start'
                                background_color: [0,1,0,1]
                                color: [0,0,0,1]
                                on_press: taskManager.relay2_start(self)
                    GridLayout:
                        cols: 1
                        Label: 
                            text: 'Relay 3' 
                        Label:
                            text: 'Preset: ' + str(app.data[6])
                        Label:
                            text: 'Extend Time: ' + str(app.data[7])
                        Label:
                            text: 'Retract Time: ' + str(app.data[8])
                        Button:
                            text: 'Manual Extend'
                            on_press: taskManager.relay3_manual_extend_retract(self)
                        Label:
                            text: 'Current Cycles: ' + str(taskManager.current_cycles_relay3) 
                        GridLayout:
                            cols: 2
                            row_default_height: 50
                            row_default_width: 50
                            row_force_defaults: True
                            Button:
                                text: 'Pause'
                                on_press: taskManager.relay3_pause(self)
                                background_color:  [1,0,0,1]
                                color: [0,0,0,1]    
                            Button: 
                                text: 'Reset'
                                background_color:  [1,0,0,1]
                                color: [0,0,0,1]
                                on_press: taskManager.relay3_reset(self)
                            Button:
                                text: 'Start'
                                background_color: [0,1,0,1]
                                color: [0,0,0,1]
                                on_press: taskManager.relay3_start(self)
                    GridLayout:
                        cols: 1
                        Label: 
                            text: 'Relay 4' 
                        Label:
                            text: 'Preset: ' + str(app.data[9])
                        Label:
                            text: 'Extend Time: ' + str(app.data[10])
                        Label:
                            text: 'Retract Time: ' + str(app.data[11])
                        Button:
                            text: 'Manual Extend'
                            on_press: taskManager.relay4_manual_extend_retract(self)
                        Label:
                            text: 'Current Cycles: ' + str(taskManager.current_cycles_relay4) 
                        GridLayout:
                            cols: 2
                            row_default_height: 50
                            row_default_width: 50
                            row_force_defaults: True
                            Button:
                                text: 'Pause'
                                on_press: taskManager.relay4_pause(self)
                                background_color:  [1,0,0,1]
                                color: [0,0,0,1]    
                            Button: 
                                text: 'Reset'
                                background_color:  [1,0,0,1]
                                color: [0,0,0,1]
                                on_press: taskManager.relay4_reset(self)
                            Button:
                                text: 'Start'
                                background_color: [0,1,0,1]
                                color: [0,0,0,1]
                                on_press: taskManager.relay4_start(self)
            Label: 
                text:''
                    
    Screen:
        name: 'taskSettings'
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Viewing Screen'
                on_press: root.current = 'taskManager'
            GridLayout:
                cols: 2
                Label: 
                    text: 'First Data:'
                TextInput:
                    text: str(app.data[0])
                    on_text: app.data[0] = int(self.text)
                Label: 
                    text: 'Second Data:'
                TextInput:
                    text: str(app.data[1])
                    on_text: app.data[1] = int(self.text)
"""
class TaskManger(Screen):
    #This is what the user inputed on the settings screen for extend time(not converted into miliseconds)
    extend_time_relay1 = 0
    extend_time_relay2 = 0
    extend_time_relay3 = 0
    extend_time_relay4 = 0
    #This is what the user inputed on the settings screen for Retract time(not converted into miliseconds)
    retract_time_relay1 = 0
    retract_time_relay2 = 0
    retract_time_relay3 = 0
    retract_time_relay4 = 0
    #The Cycle Limit for each relay this is equal to what the user set as their preset 
    cycle_limit_relay1 = 0
    cycle_limit_relay2 = 0
    cycle_limit_relay3 = 0
    cycle_limit_relay4 = 0
    #this is the time for kivyclock events
    clock_event_time = .00001 
    #The time input the user entered for extend time /1000 to make them into miliseconds, this will be put inside the controller 
    extend_time_for_controller1 = 0.0
    extend_time_for_controller2 = 0.0
    extend_time_for_controller3 = 0.0
    extend_time_for_controller4 = 0.0
    #The time input the user entered for retract time /1000 to make them into miliseconds
    retract_time_for_controller1 = 0.0
    retract_time_for_controller2 = 0.0
    retract_time_for_controller3 = 0.0
    retract_time_for_controller4 = 0.0
    #Setting the kivy clock instances so we can check to see if they exist and cancel them if they do so they don't layer on eachother

    #Current Cycles of each relay to be displayed for the user
    current_cycles_relay1 = NumericProperty(0)
    current_cycles_relay2 = NumericProperty(0)
    current_cycles_relay3 = NumericProperty(0)
    current_cycles_relay4 = NumericProperty(0)
    # 0 = was retracted, 1 = was extended, these are for manually extending and retracting the probes for calibration and other things 
    relay1_extended_or_retracted = 0
    relay2_extended_or_retracted = 0
    relay3_extended_or_retracted = 0
    relay4_extended_or_retracted = 0
    #This is too make sure that they cannot pause the clock events without having first pressing start. This stops a fatal error
    has_relay1_started = False
    has_relay2_started = False
    has_relay3_started = False 
    has_relay4_started = False 
    #Threadding stuff
    canceling_thread_relay1 = BooleanProperty(False)
    pause_thread_relay1 = BooleanProperty(False)
    thread_relay1 = ObjectProperty(allownone=True)

    canceling_thread_relay2 = BooleanProperty(False)
    pause_thread_relay2 = BooleanProperty(False)
    thread_relay2 = ObjectProperty(allownone=True)

    canceling_thread_relay3 = BooleanProperty(False)
    pause_thread_relay3 = BooleanProperty(False)
    thread_relay3 = ObjectProperty(allownone=True)

    canceling_thread_relay4 = BooleanProperty(False)
    pause_thread_relay4 = BooleanProperty(False)
    thread_relay4 = ObjectProperty(allownone=True)
    #Variables for pause checks
    is_relay1_paused = False
    is_relay2_paused = False
    is_relay3_paused = False
    is_relay4_paused = False

    def relay1_manual_extend_retract(self,instance):
        if(self.relay1_extended_or_retracted == 0):
            print("Manual Extend")
            instance.text = "Manual Retract"
            self.relay1_extended_or_retracted += 1
            #GPIO.output(Relay1, GPIO.HIGH)
        else: 
            print("Manual Retract")
            instance.text = "Manual Extend"
            self.relay1_extended_or_retracted -= 1
            #GPIO.output(Relay1, GPIO.LOW)
    
    def relay1_start(self,instance):
        if(self.has_relay1_started == False):
            print('Start Pressed')
            self.canceling_thread_relay1 = False
            if self.thread_relay1 is not None:
                return
            print('passed return')
            self.canceling_thread_relay1 = False
            self.has_relay1_started = True
            instance.text = 'STOP'
            instance.background_color = [1,0,0,1]
            self.thread_relay1 = threading.Thread(target=self.relay1_main_controller)
            self.thread_relay1.start()
            self.current_cycles_relay1 = 0
            print('completed the start func')
        elif(self.has_relay1_started == True):
            self.canceling_thread_relay1 = True
            self.current_cycles_relay1 = 0
            self.has_relay1_started = False
            instance.text = 'START'
            instance.background_color = [0,1,0,1]
            
    def relay1_reset(self,instance):
        self.current_cycles_relay1 = 0

    def cancel_thread_relay1(self):
        self.canceling_thread_relay1 = True

    def relay1_main_controller(self):
        print('thread')
        app = App.get_running_app()
        self.cycle_limit_relay1 = app.data[0]
        self.extend_time_relay1 = app.data[1]
        self.retract_time_relay1 = app.data[2]
        self.extend_time_for_controller1 = float(self.extend_time_relay1/1000)
        self.retract_time_for_controller1 = float(self.retract_time_relay1/1000)
        while not self.canceling_thread_relay1:
            if(self.is_relay1_paused == True):
                #GPIO.output(Relay1, GPIO.LOW)
                continue
            #GPIO.output(Relay1, GPIO.HIGH)
            time.sleep(self.extend_time_for_controller1)
            #GPIO.output(Relay1, GPIO.LOW)
            time.sleep(self.retract_time_for_controller1)
            self.current_cycles_relay1 += 1
            time.sleep(.2)
            if self.current_cycles_relay1 == self.cycle_limit_relay1:
                break
        self.thread_relay1 = None

    def relay1_pause(self, instance):
        if(self.has_relay1_started == True):
            if(self.is_relay1_paused == False):
                self.is_relay1_paused = True
                instance.text = 'Resume'
                instance.background_color = [0,1,0,1]
                print('Paused')
            elif(self.is_relay1_paused == True):
                self.is_relay1_paused = False
                instance.text = 'Pause'
                instance.background_color = [1,0,0,1]
                print('Resumed')
        else: 
            print("Nope")
##################################################################
    def relay2_manual_extend_retract(self,instance):
        if(self.relay2_extended_or_retracted == 0):
            print("Manual Extend")
            instance.text = "Manual Retract"
            self.relay2_extended_or_retracted += 1
            #GPIO.output(Relay2, GPIO.HIGH)
        else: 
            print("Manual Retract")
            instance.text = "Manual Extend"
            self.relay2_extended_or_retracted -= 1
            #GPIO.output(Relay2, GPIO.LOW)
    
    def relay2_start(self,instance):
        if(self.has_relay2_started == False):
            print('Start Pressed')
            self.canceling_thread_relay2 = False
            if self.thread_relay2 is not None:
                return
            print('passed return')
            self.canceling_thread_relay2 = False
            self.has_relay2_started = True
            instance.text = 'STOP'
            instance.background_color = [1,0,0,1]
            self.thread_relay2 = threading.Thread(target=self.relay2_main_controller)
            self.thread_relay2.start()
            self.current_cycles_relay2 = 0
            print('completed the start func')
        elif(self.has_relay2_started == True):
            self.canceling_thread_relay2 = True
            self.current_cycles_relay2 = 0
            self.has_relay2_started = False
            instance.text = 'START'
            instance.background_color = [0,1,0,1]
            
    def relay2_reset(self,instance):
        self.current_cycles_relay2 = 0

    def cancel_thread_relay2(self):
        self.canceling_thread_relay2 = True

    def relay2_main_controller(self):
        print('thread')
        app = App.get_running_app()
        self.cycle_limit_relay2 = app.data[3]
        self.extend_time_relay2 = app.data[4]
        self.retract_time_relay2 = app.data[5]
        self.extend_time_for_controller2 = float(self.extend_time_relay2/1000)
        self.retract_time_for_controller2 = float(self.retract_time_relay2/1000)
        while not self.canceling_thread_relay2:
            if(self.is_relay2_paused == True):
                #GPIO.output(Relay2, GPIO.LOW)
                continue
            #GPIO.output(Relay2, GPIO.HIGH)
            time.sleep(self.extend_time_for_controller2)
            #GPIO.output(Relay2, GPIO.LOW)
            time.sleep(self.retract_time_for_controller2)
            self.current_cycles_relay2 += 1
            time.sleep(.2)
            if self.current_cycles_relay2 == self.cycle_limit_relay2:
                break
        self.thread_relay2 = None

    def relay2_pause(self, instance):
        if(self.has_relay2_started == True):
            if(self.is_relay2_paused == False):
                self.is_relay2_paused = True
                instance.text = 'Resume'
                instance.background_color = [0,1,0,1]
                print('Paused')
            elif(self.is_relay2_paused == True):
                self.is_relay2_paused = False
                instance.text = 'Pause'
                instance.background_color = [1,0,0,1]
                print('Resumed')
        else: 
            print("Nope")
##########################################################################
    def relay3_manual_extend_retract(self,instance):
        if(self.relay3_extended_or_retracted == 0):
            print("Manual Extend")
            instance.text = "Manual Retract"
            self.relay3_extended_or_retracted += 1
            #GPIO.output(Relay3, GPIO.HIGH)
        else: 
            print("Manual Retract")
            instance.text = "Manual Extend"
            self.relay3_extended_or_retracted -= 1
            #GPIO.output(Relay3, GPIO.LOW)
    
    def relay3_start(self,instance):
        if(self.has_relay3_started == False):
            print('Start Pressed')
            self.canceling_thread_relay3 = False
            if self.thread_relay3 is not None:
                return
            print('passed return')
            self.canceling_thread_relay3 = False
            self.has_relay3_started = True
            instance.text = 'STOP'
            instance.background_color = [1,0,0,1]
            self.thread_relay3 = threading.Thread(target=self.relay1_main_controller)
            self.thread_relay3.start()
            self.current_cycles_relay3 = 0
            print('completed the start func')
        elif(self.has_relay1_started == True):
            self.canceling_thread_relay3 = True
            self.current_cycles_relay3 = 0
            self.has_relay3_started = False
            instance.text = 'START'
            instance.background_color = [0,1,0,1]
            
    def relay3_reset(self,instance):
        self.current_cycles_relay3 = 0

    def cancel_thread_relay3(self):
        self.canceling_thread_relay3 = True

    def relay3_main_controller(self):
        print('thread')
        app = App.get_running_app()
        self.cycle_limit_relay3 = app.data[6]
        self.extend_time_relay3 = app.data[7]
        self.retract_time_relay3 = app.data[8]
        self.extend_time_for_controller3 = float(self.extend_time_relay3/1000)
        self.retract_time_for_controller3 = float(self.retract_time_relay3/1000)
        while not self.canceling_thread_relay3:
            if(self.is_relay3_paused == True):
                #GPIO.output(Relay3, GPIO.LOW)
                continue
            #GPIO.output(Relay3, GPIO.HIGH)
            time.sleep(self.extend_time_for_controller3)
            #GPIO.output(Relay3, GPIO.LOW)
            time.sleep(self.retract_time_for_controller3)
            self.current_cycles_relay3 += 1
            time.sleep(.2)
            if self.current_cycles_relay3 == self.cycle_limit_relay3:
                break
        self.thread_relay3 = None

    def relay3_pause(self, instance):
        if(self.has_relay3_started == True):
            if(self.is_relay3_paused == False):
                self.is_relay3_paused = True
                instance.text = 'Resume'
                instance.background_color = [0,1,0,1]
                print('Paused')
            elif(self.is_relay3_paused == True):
                self.is_relay3_paused = False
                instance.text = 'Pause'
                instance.background_color = [1,0,0,1]
                print('Resumed')
        else: 
            print("Nope")
###############################################################################
    def relay4_manual_extend_retract(self,instance):
        if(self.relay4_extended_or_retracted == 0):
            print("Manual Extend")
            instance.text = "Manual Retract"
            self.relay4_extended_or_retracted += 1
            #GPIO.output(Relay4, GPIO.HIGH)
        else: 
            print("Manual Retract")
            instance.text = "Manual Extend"
            self.relay4_extended_or_retracted -= 1
            #GPIO.output(Relay4, GPIO.LOW)
    
    def relay4_start(self,instance):
        if(self.has_relay4_started == False):
            print('Start Pressed')
            self.canceling_thread_relay4 = False
            if self.thread_relay4 is not None:
                return
            print('passed return')
            self.canceling_thread_relay4 = False
            self.has_relay4_started = True
            instance.text = 'STOP'
            instance.background_color = [1,0,0,1]
            self.thread_relay4 = threading.Thread(target=self.relay1_main_controller)
            self.thread_relay4.start()
            self.current_cycles_relay4 = 0
            print('completed the start func')
        elif(self.has_relay4_started == True):
            self.canceling_thread_relay4 = True
            self.current_cycles_relay4 = 0
            self.has_relay4_started = False
            instance.text = 'START'
            instance.background_color = [0,1,0,1]
            
    def relay4_reset(self,instance):
        self.current_cycles_relay4 = 0

    def cancel_thread_relay4(self):
        self.canceling_thread_relay4 = True

    def relay4_main_controller(self):
        print('thread')
        app = App.get_running_app()
        self.cycle_limit_relay4 = app.data[9]
        self.extend_time_relay4 = app.data[10]
        self.retract_time_relay4 = app.data[11]
        self.extend_time_for_controller4 = float(self.extend_time_relay1/1000)
        self.retract_time_for_controller4 = float(self.retract_time_relay1/1000)
        while not self.canceling_thread_relay4:
            if(self.is_relay4_paused == True):
                #GPIO.output(Relay4, GPIO.LOW)
                continue
            #GPIO.output(Relay4, GPIO.HIGH)
            time.sleep(self.extend_time_for_controller4)
            #GPIO.output(Relay4, GPIO.LOW)
            time.sleep(self.retract_time_for_controller4)
            self.current_cycles_relay4 += 1
            time.sleep(.2)
            if self.current_cycles_relay4 == self.cycle_limit_relay4:
                break
        self.thread_relay4 = None

    def relay4_pause(self, instance):
        if(self.has_relay4_started == True):
            if(self.is_relay4_paused == False):
                self.is_relay4_paused = True
                instance.text = 'Resume'
                instance.background_color = [0,1,0,1]
                print('Paused')
            elif(self.is_relay1_paused == True):
                self.is_relay1_paused = False
                instance.text = 'Pause'
                instance.background_color = [1,0,0,1]
                print('Resumed')
        else: 
            print("Nope")

class Test(App):
    data = ListProperty()
    def build(self):
        self.load_data()
        return Builder.load_string(KV)
    def load_data(self):
        #would actually load data from the txt file, just filling it temporarily here
        self.data = [100,200,200,100,500,500,100,500,500,100,500,500]

    def on_data(self, *_):
        #would actually save self.data to the text file
        pass

if __name__ == '__main__':
    Test().run()
