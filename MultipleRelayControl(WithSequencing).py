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
#import RPi.GPIO as GPIO
"""
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

Relay1 = 37
Relay2 = 33
Relay3 = 36
Relay4 = 18

GPIO.setup(Relay1, GPIO.OUT)
GPIO.setup(Relay2, GPIO.OUT)
GPIO.setup(Relay3, GPIO.OUT)
GPIO.setup(Relay4, GPIO.OUT)

GPIO.output(Relay1, GPIO.LOW)
GPIO.output(Relay2, GPIO.LOW)
GPIO.output(Relay3, GPIO.LOW)
GPIO.output(Relay4, GPIO.LOW)
"""
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
                on_press: root.current = 'relaySettings'
            Label:
                text: ''
            Label:
                text: ''
            Button:
                size_hint_x: 0.5
                size_hint_y: .9
                text: 'Sequence Settings'
                font_size: 18
                on_press: root.current = 'sequenceSettings'
            Label:
                text:''
            Label: 
                text: ''
            Button:
                size_hint_x: 0.5
                size_hint_y: .9
                text: 'Sequence Manager'
                font_size: 18
                on_press: root.current = 'sequenceManager'
            Label:
                text: 'Current kivy test version'

    TaskManger:
        name: 'taskManager'
        id: taskManager 
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: .3
                height: 105
                Image: 
                    source: 'logo.png'      
                Label:
                    text: 'Task Manager'
                    font_size: '28'
                    bold: True
                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Task Settings'
                    font_size: 16
                    on_press: root.current = 'relaySettings'
                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Main Menu'
                    font_size: 16
                    on_press: root.current = 'mainMenu'
            GridLayout:
                cols: 4
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
                    cols: 4
                    rows: 1
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
                    cols: 4
                    rows: 1
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
                    cols: 4
                    rows: 1
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
                    size: 100,100
                    text: ''
                    size_hint_y: 0.4
                Label:
                    size: 100,100
                    text: ''
                    size_hint_y: 0.4                
                Label:
                    size: 100,100
                    text: ''
                    size_hint_y: 0.4
                Label:
                    size: 100,100
                    text: 'Pressure: '
                    size_hint_y: 0.4

    RelaySettings:
        name: 'relaySettings'
        id: relaySettings
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: .3
                height: 105
                Image: 
                    source: 'logo.png'      
                Label:
                    text: 'Relay Settings'
                    font_size: '28'
                    bold: True
                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Task Manager'
                    font_size: 16
                    on_press: root.current = 'taskManager'
                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Sequence Settings'
                    font_size: 12
                    on_press: root.current = 'sequenceSettings'
                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Main Menu'
                    font_size: 16
                    on_press: root.current = 'mainMenu'
            GridLayout:
                cols: 6
                size_hint_y: .1
                Button:
                    text: 'Relay 1'
                    size_hint_y: .3
                    size_hint_x: .3
                    on_press: relaySettings.relay1_select(self)
                Button:
                    text: 'Relay 2'
                    size_hint_y: .3
                    size_hint_x: .3
                    on_press: relaySettings.relay2_select(self)
                Button:
                    text: 'Relay 3'
                    size_hint_y: .3
                    size_hint_x: .3
                    on_press: relaySettings.relay3_select(self)
                Button:
                    text: 'Relay 4'
                    size_hint_y: .3
                    size_hint_x: .3
                    on_press: relaySettings.relay4_select(self)

                Label:
                    text: ''
                Label:
                    text: ''

            GridLayout:
                cols: 3

                Label:
                    text: 'Preset: '
                    size_hint_y: .3
                    size_hint_x: .7
                CustomTextInput:
                    text: ''
                    size_hint_y: .3
                    size_hint_x: .7
                    on_text: relaySettings.preset_field = int(self.text) if len(self.text) > 0 else 0

                Label:
                    text: 'Current Relay: Relay ' + str(relaySettings.current_relay) 
                    size_hint_y: .3
                    size_hint_x: .7
                Label:
                    text: 'Extend Time: '
                    size_hint_y: .3
                    size_hint_x: .7
                CustomTextInput:
                    text: ''
                    size_hint_y: .3
                    size_hint_x: .7
                    on_text: relaySettings.extend_field = int(self.text) if len(self.text) > 0 else 0

                Label:
                    text: ''
                    size_hint_y: .3
                    size_hint_x: .7
                Label:
                    text: 'Retract Time: '
                    size_hint_y: .3
                    size_hint_x: .7
                CustomTextInput:
                    text: '' 
                    size_hint_y: .3
                    size_hint_x: .7
                    on_text: relaySettings.retract_field = int(self.text) if len(self.text) > 0 else 0

                Button:
                    text: 'Submit'
                    size_hint_y: .3
                    size_hint_x: .7
                    on_press: relaySettings.submit(self)
    SequenceSettings:
        name: 'sequenceSettings'
        id: sequenceSettings
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: .3
                height: 105
                Image: 
                    source: 'logo.png'      
                Label:
                    text: 'Sequence Settings'
                    font_size: '28'
                    bold: True
                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Relay Settings'
                    font_size: 16
                    on_press: root.current = 'relaySettings'

                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Main Menu'
                    font_size: 16
                    on_press: root.current = 'mainMenu'
            GridLayout:
                cols: 6
                size_hint_y: .1
                Button:
                    text: 'Relay 1'
                    size_hint_y: .3
                    size_hint_x: .3
                    on_press: sequenceSettings.relay1_select(self)
                Button:
                    text: 'Relay 2'
                    size_hint_y: .3
                    size_hint_x: .3
                    on_press: sequenceSettings.relay2_select(self)
                Button:
                    text: 'Relay 3'
                    size_hint_y: .3
                    size_hint_x: .3
                    on_press: sequenceSettings.relay3_select(self)
                Button:
                    text: 'Relay 4'
                    size_hint_y: .3
                    size_hint_x: .3
                    on_press: sequenceSettings.relay4_select(self)

                Label:
                    text: ''
                Label:
                    text: ''

            GridLayout:
                cols: 3

                Label:
                    text: 'Amount of Cycles: '
                    size_hint_y: .3
                    size_hint_x: .7
                CustomTextInput:
                    text: ''
                    size_hint_y: .3
                    size_hint_x: .7
                    on_text: sequenceSettings.sequence_cycles_field = int(self.text) if len(self.text) > 0 else 0

                Label:
                    text: ''  
                    size_hint_y: .3
                    size_hint_x: .7
                Label:
                    text: 'Total Time of Sequence:'
                    size_hint_y: .3
                    size_hint_x: .7
                CustomTextInput:
                    text: ''
                    size_hint_y: .3
                    size_hint_x: .7
                    on_text: sequenceSettings.sequence_time_field = int(self.text) if len(self.text) > 0 else 0
                Button:
                    text: 'Submit Sequence'
                    size_hint_y: .3
                    size_hint_x: .7
                    on_press: sequenceSettings.sequence_submit(self)


                Label:
                    text: 'Start Time of relay ' + str(sequenceSettings.current_relayS) + ' in the sequence'
                    size_hint_y: .3
                    size_hint_x: .7
                CustomTextInput:
                    text: '' 
                    size_hint_y: .3
                    size_hint_x: .7
                    on_text: sequenceSettings.relay_start_time_field = int(self.text) if len(self.text) > 0 else 0

                Button:
                    text: 'Submit Relay'
                    size_hint_y: .3
                    size_hint_x: .7
                    on_press: sequenceSettings.relay_submit(self)
    SequenceManager:
        name: 'sequenceManager'
        id: sequenceManager

        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: .3
                height: 105
                Image: 
                    source: 'logo.png'      
                Label:
                    text: 'Sequence Manager'
                    font_size: '28'
                    bold: True
                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Sequence Settings'
                    font_size: 16
                    on_press: root.current = 'sequenceSettings'

                Button:
                    size_hint_x: 0.5
                    size_hint_y: .9
                    text: 'Main Menu'
                    font_size: 16
                    on_press: root.current = 'mainMenu'
            GridLayout:
                cols: 3
                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        text: "Relay 1 time in sequence " + str(app.seqData[2])
                    Label:
                        text: "Relay 2 time in sequence " + str(app.seqData[3])
                    Label:
                        text: "Relay 3 time in sequence " + str(app.seqData[4])
                    Label:
                        text: "Relay 4 time in sequence " + str(app.seqData[5])
                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        text: ''
                    Label: 
                        text: 'Current Time ' + str(sequenceManager.current_time_in_cycle)
                    Label: 
                        text: 'Current Cycles '  + str(sequenceManager.current_cycles)
                Label: 
                    text: 'Times are in 10ths of a second'
                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        text: ''
                    Label: 
                        text: 'Total Time of one sequence ' + str(app.seqData[1])
                    Label: 
                        text: 'Amount of Cycles to be ran '  + str(app.seqData[0])
                Label: 
                    text: 'Current Relay Fired ' + str(sequenceManager.relay_fired)
                GridLayout:
                    cols: 2
                    row_default_height: 50
                    row_default_width: 50
                    row_force_defaults: True
                    Button:
                        text: 'Pause'
                        on_press: sequenceManager.pause_pressed(self)
                        background_color:  [1,0,0,1]
                        color: [0,0,0,1]    
                    Button: 
                        text: 'Reset'
                        background_color:  [1,0,0,1]
                        color: [0,0,0,1]
                        on_press: sequenceManager.reset_pressed(self)
                    Button:
                        text: 'Start'
                        background_color: [0,1,0,1]
                        color: [0,0,0,1]
                        on_press: sequenceManager.start_pressed(self)
"""
class SequenceManager(Screen):
    #Setting Inital Values for Threads(They most be set too None when initalizing so you can stop multiple istances of the same thread existing and hanging and draining preformance)
    thread_master_sequence = None
    thread_relay1_FIRE = None
    thread_relay2_FIRE = None
    thread_relay3_FIRE = None
    thread_relay4_FIRE = None
    #thread variables for controll
    canceling_thread_master_sequence = BooleanProperty(False)
    pause_thread_master_sequence = BooleanProperty(False)
    thread_master_sequence = ObjectProperty(allownone = True)
    canceling_thread_relay1_FIRE = BooleanProperty(False)
    thread_relay1_FIRE = ObjectProperty(allownone=True)
    canceling_thread_relay2_FIRE = BooleanProperty(False)
    thread_relay2_FIRE = ObjectProperty(allownone=True)
    canceling_thread_relay3_FIRE = BooleanProperty(False)
    thread_relay3_FIRE = ObjectProperty(allownone=True)
    canceling_thread_relay4_FIRE = BooleanProperty(False)
    thread_relay4_FIRE = ObjectProperty(allownone=True)
    #Variables for Relay settings
    extend_time_relay1 = 0.0
    retract_time_relay1 = 0.0
    extend_time_relay2 = 0.0
    retract_time_relay2 = 0.0
    extend_time_relay3 = 0.0
    retract_time_relay3 = 0.0
    extend_time_relay4 = 0.0
    retract_time_relay4 = 0.0   
    #Variables for Relay Sequence
    sequence_time_relay1 = 0.0
    sequence_time_relay2 = 0.0
    sequence_time_relay3 = 0.0
    sequence_time_relay4 = 0.0
    #UI variables need to be assigned to a kivy property 
    sequence_time_master = 0.0
    sequence_cycle = 0 
    current_time_in_cycle = NumericProperty(0.0)
    current_cycles = NumericProperty(0)
    relay_fired = NumericProperty(0)
    start_pressed_bool = False
    paused_bool = False
    def start_pressed(self,instance):
        app = App.get_running_app()
        #Setting the extend & retract times for the relays
        self.extend_time_relay1 = float(app.data[1]/1000)
        self.retract_time_relay1 = float(app.data[2]/1000)
        self.extend_time_relay2 = float(app.data[4]/1000)
        self.retract_time_relay2 = float(app.data[5]/1000)
        self.extend_time_relay3 = float(app.data[7]/1000)
        self.retract_time_relay3 = float(app.data[8]/1000)
        self.extend_time_relay4 = float(app.data[10]/1000)
        self.retract_time_relay4 = float(app.data[11]/1000)
        #Setting the sequence fire time for each relay 
        self.sequence_time_relay1 = float(app.seqData[2])
        self.sequence_time_relay2 = float(app.seqData[3])
        self.sequence_time_relay3 = float(app.seqData[4])
        self.sequence_time_relay4 = float(app.seqData[5])
        print(self.sequence_time_relay1)
        #Setting Sequence Cycle Cap & Cycle Time
        self.sequence_cycle = float(app.seqData[0])
        self.sequence_time_master = float(app.seqData[1])
        print("Start Started")
        if(self.start_pressed_bool == False):
            print('Start Pressed')
            self.canceling_thread_relay1 = False
            if self.thread_master_sequence is not None:
                return
            print('passed return')
            self.canceling_thread_relay1 = False
            self.start_pressed_bool = True
            instance.text = 'STOP'
            instance.background_color = [1,0,0,1]
            self.thread_master_sequence = threading.Thread(target=self.sequence_master)
            self.thread_master_sequence.start()
            self.current_cycles_relay1 = 0
            print('completed the start func')
        elif(self.start_pressed_bool == True):
            print("start has already been pressed")
            self.canceling_thread_master_sequence = True
            self.current_cycles = 0
            self.start_pressed_bool = False
            instance.text = 'START'
            instance.background_color = [0,1,0,1]
            

    def pause_pressed(self,instance):
        if(self.start_pressed_bool == True):
            if(self.paused_bool == False):
                self.paused_bool = True
                instance.text = 'Resume'
                instance.background_color = [0,1,0,1]
                print('Paused')
            elif(self.paused_bool == True):
                self.paused_bool = False
                instance.text = 'Pause'
                instance.background_color = [1,0,0,1]
                print('Resumed')
    def reset_pressed(self,instance): #This sets the current cycles that the user sees back to 0 when the button is pressed 
        self.current_cycles = 0 
        print("Sequence Reset") 
    def canceling_thread_master_sequence1(self):
        self.canceling_thread_master_sequence = True
    def sequence_master(self):
        while not self.canceling_thread_master_sequence:
            if(self.paused_bool == True):
                continue
            if(self.current_time_in_cycle == self.sequence_time_relay1):
                self.thread_relay1_FIRE = threading.Thread(target=self.relay1)
                self.thread_relay1_FIRE.start()
                self.relay_fired = 1
                time.sleep(.1)
                self.current_time_in_cycle += .1
                self.current_time_in_cycle = round(self.current_time_in_cycle,1)
            elif(self.current_time_in_cycle == self.sequence_time_relay2):
                self.thread_relay2_FIRE = threading.Thread(target=self.relay2)
                self.thread_relay2_FIRE.start()
                self.relay_fired = 2
                time.sleep(.1)
                self.current_time_in_cycle += .1
                self.current_time_in_cycle = round(self.current_time_in_cycle,1)
            elif(self.current_time_in_cycle == self.sequence_time_relay3):
                self.thread_relay3_FIRE = threading.Thread(target=self.relay3)
                self.thread_relay3_FIRE.start()
                self.relay_fired = 3
                time.sleep(.1)
                self.current_time_in_cycle += .1
                self.current_time_in_cycle = round(self.current_time_in_cycle,1)
            elif(self.current_time_in_cycle == self.sequence_time_relay4):
                self.thread_relay4_FIRE = threading.Thread(target=self.relay4)
                self.thread_relay4_FIRE.start()
                self.relay_fired = 4
                time.sleep(.1)
                self.current_time_in_cycle += .1
                self.current_time_in_cycle = round(self.current_time_in_cycle,1)
            elif(self.current_time_in_cycle == self.sequence_time_master):
                self.current_cycles += 1
                time.sleep(.1)
                self.current_time_in_cycle = .1
                self.current_time_in_cycle = round(self.current_time_in_cycle,1)
            else:
                time.sleep(.1)
                self.current_time_in_cycle += .1
                self.current_time_in_cycle = round(self.current_time_in_cycle,1)
            if(self.current_cycles == self.sequence_cycle):
                self.canceling_thread_master_sequence1()
                break 
    def relay1(self):
        print('relay1 fired')
        #GPIO.output(Relay1,GPIO.HIGH)
        time.sleep(self.extend_time_relay1)
        #GPIO.output(Relay1,GPIO.LOW)
        time.sleep(self.retract_time_relay1)
        self.relay_fired = 0 
    def relay2(self):
        print('relay2 fired')
        #GPIO.output(Relay2,GPIO.HIGH)
        time.sleep(self.extend_time_relay2)
        #GPIO.output(Relay2,GPIO.LOW)
        time.sleep(self.retract_time_relay2)
        self.relay_fired = 0
    def relay3 (self):
        print('relay3 fired')
        #GPIO.output(Relay3,GPIO.HIGH)
        time.sleep(self.extend_time_relay3)
        #GPIO.output(Relay3,GPIO.LOW)
        time.sleep(self.retract_time_relay3)
        self.relay_fired = 0     
    def relay4(self):
        print('relay4 fired')
        #GPIO.output(Relay4,GPIO.HIGH)
        time.sleep(self.extend_time_relay4)
        #GPIO.output(Relay4,GPIO.LOW)
        time.sleep(self.retract_time_relay4)
        self.relay_fired = 0
class SequenceSettings(Screen):
    relay_start_time_field = 0
    sequence_time_field = 0
    sequence_cycles_field = 0
    sequence_cycle = NumericProperty(0)
    sequence_time = NumericProperty(0)
    relay1_start_time = NumericProperty(0)
    relay2_start_time = NumericProperty(0)
    relay3_start_time = NumericProperty(0)
    relay4_start_time = NumericProperty(0)
    current_relayS = NumericProperty(0)

    def relay1_select(self,instance):
        self.current_relayS = 1
    def relay2_select(self,instance):
        self.current_relayS = 2
    def relay3_select(self,instance):
        self.current_relayS = 3
    def relay4_select(self,instance):
        self.current_relayS = 4
    def sequence_submit(self,instance):#function for kivy button widget, refrenced via instance and binded to widget in kivy  builder
        app = App.get_running_app() #Grabs the App class so we can refrence lists so we can store user input to memory 
        self.sequence_cycle = self.sequence_cycles_field #setting entry fields into a local variable to then be appended to a array to be refrenced later
        self.sequence_time = self.sequence_time_field
        #making sure it passes and the data input is also fine 
        print(self.sequence_cycles_field)
        print(self.sequence_time_field)
        if(self.sequence_time & self.sequence_cycle != 0): 
            app.seqData[0] = self.sequence_cycle #Sequence Cycles user input is appended to a list as entry 0 to be refrenced later(in memory)
            app.seqData[1] = self.sequence_time #Sequence Time user input is appended to a list as entry 1 to be refrenced later(in memory)
            print('Sequence start and cycle Data Stored to memory')#Making sure it passes to the print statement 
    def relay_submit(self,instance):
        app = App.get_running_app()#Grabs the App class so we can refrence lists so we can store user input to memory 
        if(self.current_relayS == 1):#Checks which relay button  ustheer pressed and applies data accordingly
            self.relay1_start_time = self.relay_start_time_field #Converts the data from the Custom TextBox Kivy Widget into a local variable so we can append it to the list in the app memory
            app.seqData[2] = self.relay1_start_time#User input in relay num field appended into a list in the memory as entry 2
        elif(self.current_relayS == 2):#Checks which relay button the user pressed and applies data accordingly
            self.relay2_start_time = self.relay_start_time_field #Converts the data from the Custom TextBox Kivy Widget into a local variable so we can append it to the list in the app memory
            app.seqData[3] = self.relay2_start_time#User input in relay num field appended into a list in the memory as entry 3
        elif(self.current_relayS == 3):#Checks which relay button  ustheer pressed and applies data accordingly
            self.relay3_start_time = self.relay_start_time_field #Converts the data from the Custom TextBox Kivy Widget into a local variable so we can append it to the list in the app memory
            app.seqData[4] = self.relay3_start_time#User input in relay num field appended into a list in the memory as entry 4
        elif(self.current_relayS == 4):#Checks which relay button  ustheer pressed and applies data accordingly
            self.relay4_start_time = self.relay_start_time_field#Converts the data from the Custom TextBox Kivy Widget into a local variable so we can append it to the list in the app memory
            app.seqData[5] = self.relay4_start_time#User input in relay num field appended into a list in the memory as entry 5
        #checking if everything is doing what it is supposed to 
        print(self.relay_start_time_field)
        print(app.seqData)
class RelaySettings(Screen):
    preset_field = 0
    extend_field = 0
    retract_field = 0
    current_relay = NumericProperty(0) #UI Variables need to be assigned to a kivy property 
    def relay1_select(self,instance):
        self.current_relay = 1
    def relay2_select(self,instance):
        self.current_relay = 2
    def relay3_select(self,instance):
        self.current_relay = 3
    def relay4_select(self,instance):
        self.current_relay = 4
    def submit(self,instance):
        app = App.get_running_app()
        if(self.current_relay == 1):
            if(self.preset_field & self.extend_field & self.retract_field != 0):
                app.data[0] = self.preset_field
                app.data[1] = self.extend_field
                app.data[2] = self.retract_field
        elif(self.current_relay == 2):
            if(self.preset_field & self.extend_field & self.retract_field != 0):
                app.data[3] = self.preset_field
                app.data[4] = self.extend_field
                app.data[5] = self.retract_field
        elif(self.current_relay == 3):
            if(self.preset_field & self.extend_field & self.retract_field != 0):
                app.data[6] = self.preset_field
                app.data[7] = self.extend_field
                app.data[8] = self.retract_field
        elif(self.current_relay == 4):
            if(self.preset_field & self.extend_field & self.retract_field != 0):
                app.data[9] = self.preset_field
                app.data[10] = self.extend_field
                app.data[11] = self.retract_field
        else:
            print('None')
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
            self.thread_relay3 = threading.Thread(target=self.relay3_main_controller)
            self.thread_relay3.start()
            self.current_cycles_relay3 = 0
            print('completed the start func')
        elif(self.has_relay3_started == True):
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
            self.thread_relay4 = threading.Thread(target=self.relay4_main_controller)
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
            elif(self.is_relay4_paused == True):
                self.is_relay4_paused = False
                instance.text = 'Pause'
                instance.background_color = [1,0,0,1]
                print('Resumed')
        else: 
            print("Nope")
class CustomTextInput(TextInput):
    def on_keyboard(self, instance, value):
        if self.keyboard.widget:
            vkeyboard = self.keyboard.widget
            vkeyboard.layout = 'keynums.json'
class Test(App):
    data = ListProperty()
    seqData = ListProperty()
    def build(self):
        self.load_data()
        self.load_seqData()
        return Builder.load_string(KV)
    def load_data(self):
        #would actually load data from the txt file, just filling it temporarily here
        self.data = [100,200,200,100,500,500,100,500,500,100,500,500]
    def on_data(self, *_):
        #would actually save self.data to the text file
        pass
    def load_seqData(self):
        self.seqData = [0,0,0,0,0,0]
if __name__ == '__main__':
    Test().run()
