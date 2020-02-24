import os
import time
import RPi.GPIO as GPIO
import kivy
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics','width','480')
Config.set('graphics','height','272')
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
Window.fullscreen = True 

relay_control = 0 
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

GPIO.output(Relay1, GPIO.HIGH)
GPIO.output(Relay2, GPIO.HIGH)
GPIO.output(Relay3, GPIO.HIGH)
GPIO.output(Relay4, GPIO.HIGH)

class Interact(GridLayout):
    applyclicked = False

    tooFastArray = []
    for i in range(-1,100):
        tooFastArray.append(str(i))

    extendRetract = 0.0

    relay_master = 0
    relay_control1 = 0.0
    relay_control2 = 0.0
    relay_control3 = 0.0

    cycle_count = None
    relayMasterController = None

    cycleCap = 0
    cycles = 0
    extendTimeGlobal = 0.0
    retractTimeGlobal = 0.0
    cycleTimeGlobal = 0.0
    constantGlobal = 0.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.part1 = GridLayout(cols=2, row_force_default=True, row_default_height=100,rows = 6,spacing = [1,1])
        
        self.part2 = GridLayout(cols=4, row_force_default=True, row_default_height=65,rows = 2)
    

        if os.path.isfile("prev_details.txt"):#Saves previous input to a txt file and redisplays it on launch
           with open("prev_details.txt", "r") as f:
            d = f.read().split(",")
            prev_preset = d[0]
            prev_timeE = d[1]
            prev_timeR = d[2]

        else:
            prev_preset = ""
            prev_timeE = ""
            prev_timeR = ""
        self.logo = Image(source=('logo.png'))
        self.part1.add_widget(self.logo)

        self.part1.add_widget(Label(text=('Minimum Time is 100 miliseconds, Max is 1,000,000\nMinimum Preset is 0, Max is 100,000,000,000'),font_size = 16))

        self.part1.PresetL =Label(text=("Preset:\n" + prev_preset),font_size = 18)
        self.part1.add_widget(self.part1.PresetL)
        self.part1.Preset = CustomTextInput(text= (prev_preset),multiline=False, background_color = [1,1,1,.95], width= 90, height = 50 )
        self.part1.add_widget(self.part1.Preset)
        
        self.part1.extendTimeL = Label(text=("Time to Extend:\n" + prev_timeE+"ms"),font_size = 18,height = 40)
        self.part1.add_widget(self.part1.extendTimeL)
        self.part1.extendTimeI = CustomTextInput(text=(prev_timeE), multiline=False, background_color = [1,1,1,.95], width= 90, height = 50)
        self.part1.add_widget(self.part1.extendTimeI)

        self.part1.retractTimeL = Label(text=("Time to Retract:\n"+prev_timeR + "ms"),font_size = 18, height = 4)
        self.part1.add_widget(self.part1.retractTimeL)
        self.part1.retractTimeI = CustomTextInput(text=(prev_timeE), multiline=False, background_color = [1,1,1,.95], width= 200, height = 200)
        self.part1.add_widget(self.part1.retractTimeI)

        self.part1.Ct = Label(text=("Current Cycles:\n"),font_size = 18)
        self.part1.add_widget(self.part1.Ct)

        self.Apply = Button(text = "Apply",font_size = 40) 
        self.Apply.bind(on_press=self.Apply_Button)
        self.part1.add_widget(self.Apply)

        self.add_widget(self.part1)
        
        self.Pause = Button(text=("Pause"),font_size = 25,size_hint_x=10, width=90,height=40)
        self.part2.add_widget(self.Pause)
        self.Pause.bind(on_press = self.Pause_Button)

        self.Reset = Button(text=("Reset"),font_size = 25,size_hint_x=10, width=90,height=40)
        self.part2.add_widget(self.Reset)
        self.Reset.bind(on_press = self.Reset_Button)
        self.manual_re= Button(text="Manual Extend",font_size = 19,size_hint_x=10, width= 90, height = 40)
        self.part2.add_widget(self.manual_re)
        self.manual_re.bind(on_press = self.manual_extend_retract)
        self.part2.add_widget(Label(text=('')))
    
        self.part1.add_widget(self.part2)

    def Apply_Button(self, instance):

        self.part1.PresetG = self.part1.Preset.text#grabbing data from the fields to save
        self.part1.extendTimeIU = self.part1.extendTimeI.text
        self.part1.retractTimeIU = self.part1.retractTimeI.text
        if (self.part1.PresetG == ''):
            print("No fields Full Preset")
        elif(self.part1.extendTimeIU == ''):
            print("No fields Full Cycle Time")
        elif(self.part1.extendTimeIU in self.tooFastArray):
            print("Too Fast Slow Down")
        elif(self.part1.extendTimeIU == '0'):
            print("sorry but 0 is not vaild")
        elif(self.part1.retractTimeIU == ''):
            print("No fields Full Cycle Time")
        elif(self.part1.retractTimeIU in self.tooFastArray):
            print("Too Fast Slow Down")
        elif(self.part1.retractTimeIU == '0'):
            print("sorry but 0 is not vaild")
        else:
            self.user_input_extend = int(self.part1.extendTimeIU)
            self.user_input_retract = int(self.part1.retractTimeIU)
            self.cycleCap = int(self.part1.PresetG)

            if(self.cycleCap >= 1000000000001):
                print("Too Big Preset")
            elif(self.user_input_extend >= 1000001):
                print("Too Big Time")
            elif(self.user_input_retract >= 1000001):
                print("Too Big Time")
            elif(self.cycleCap <= 0):
                print("Too little Preset")
            elif(self.user_input_extend <= 0):
                print("Too little Time")
            elif(self.user_input_retract <= 0):
                print("Too little Time")
            else:
                if self.relayMasterController:
                    self.relayMasterController.cancel()
                self.cycles = 0

                self.part1.PresetL.text = ("Preset:\n" + self.part1.PresetG)
                self.part1.extendTimeL.text = ("Extend Time:\n" + self.part1.extendTimeIU + "ms") 
                self.part1.retractTimeL.text = ("Retract Time:\n" + self.part1.retractTimeIU + "ms")

                #self.user_input_timef = float(self.user_input_timei/1000)
                #self.relay_wacker = float(self.user_input_timef/2)
                self.constantGlobal = float(0.00001)
                self.extendTimeGlobal = float(self.user_input_extend/1000)
                self.retractTimeGlobal = float(self.user_input_retract/1000)
                self.cycleTimeGlobal = float(self.extendTimeGlobal + self.retractTimeGlobal)
                print(self.extendTimeGlobal)
                print(self.retractTimeGlobal)
                self.applyclicked = True
                self.relayMasterController = Clock.schedule_interval(self.relay_controller,self.constantGlobal)
                

                with open("prev_details.txt", "w") as f:#Writing previous input to local txt file
                    f.write(f"{self.part1.PresetG},{self.part1.extendTimeIU},{self.part1.retractTimeIU}")

    def relay_controller(self, dt):
        if(self.relay_master == 0):
            self.relay_control1 += 0.01
            print(self.relay_control1)
            if(self.relay_control1 <= self.extendTimeGlobal):
                print("Current Extend")
                GPIO.output(Relay1, GPIO.HIGH)
                GPIO.output(Relay2, GPIO.HIGH)
                GPIO.output(Relay3, GPIO.HIGH)
                GPIO.output(Relay4, GPIO.HIGH)
            else:
                print("switching")
                self.relay_master += 1
                self.relay_control1 = 0.0

        elif(self.relay_master == 1):
            self.relay_control2 += 0.01
            print(self.relay_control2)
            if(self.relay_control2 <= self.retractTimeGlobal):
                print("Current Retract")
                GPIO.output(Relay1, GPIO.LOW)
                GPIO.output(Relay2, GPIO.LOW)
                GPIO.output(Relay3, GPIO.LOW)
                GPIO.output(Relay4, GPIO.LOW)
            else:
                print("switching")
                self.relay_master += 1
                self.relay_control2 = 0.0 
        elif(self.relay_master == 2):
            self.cycles += 1    
            self.part1.Ct.text = "Current Cycles: " + str(self.cycles) + "\nPreset: " + str(self.cycleCap)
            if(self.cycles == self.cycleCap):
                self.relayMasterController.cancel()
            else:
                self.relay_master -= 2
                print("Completed 1 Cycle")


    def cycle_updater(self, dt):

        self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.cycleCap)
        self.part1.cycles += 1
        if(int(self.part1.cycles) == int(self.cycleCap)):
            self.cycle_count.cancel()
  

    def Pause_Button(self,instance):
        if(self.applyclicked == False):
            print("Nope")
        else:
            if self.relayMasterController:
                self.relayMasterController.cancel()
                self.relayMasterController = None

                self.part1.Ct.text = "Current Cycles: " + str(self.cycles) + "\nPreset: " + str(self.cycleCap) + "\nPaused"
                self.Pause.text = "Resume"   
                print("PAUSED")         
            else:
                self.relayMasterController = Clock.schedule_interval(self.relay_controller,self.constantGlobal)
                self.Pause.text = "Pause"
                print("RESUME")
           
    def Reset_Button(self,instance):
        if(self.cycleCap == 0):
            print("NO RESET")
        else:
            self.part1.cycles = 0
            print("RESETED")
            if self.cycle_count: 
                self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.cycleCap)
            else:
                self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.cycleCap) + "\nPaused"



    def manual_extend_retract(self,isinstance):
        if(self.extendRetract == 0):
            print("Manual Extend")
            self.manual_re.text = "Manual Retract"
            self.extendRetract += 1
            GPIO.output(Relay1, GPIO.HIGH)
            GPIO.output(Relay2, GPIO.HIGH)
            GPIO.output(Relay3, GPIO.HIGH)
            GPIO.output(Relay4, GPIO.HIGH)

        else: 
            print("Manual Retract")
            self.manual_re.text = "Manual Extend"
            self.extendRetract -= 1
            GPIO.output(Relay1, GPIO.LOW)
            GPIO.output(Relay2, GPIO.LOW)
            GPIO.output(Relay3, GPIO.LOW)
            GPIO.output(Relay4, GPIO.LOW)

           
"""class Keypad(GridLayout):
    def __init__(self, *args, **kwargs)
        self.cols = 3
        self.spacing = 10 
        self.createNums()
    def createNums(self):
        nums = [1,2,3,4,5,6,7,8,9,0]
        for i in nums"""


class CustomTextInput(TextInput):
    def on_keyboard(self, instance, value):
        if self.keyboard.widget:
            vkeyboard = self.keyboard.widget
            vkeyboard.layout = 'keynums.json'
        
class GUI(App):
    def build(self):

        return Interact()

if __name__ =="__main__":

    GUI().run() 
