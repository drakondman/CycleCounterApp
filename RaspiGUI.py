import os
import time
import kivy
import RPi.GPIO as GPIO
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
Window.fullscreen = True

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

class Interact(GridLayout):
    cycle_count = None
    relay_low = None
    relay_control = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.part1 = GridLayout()
        self.part1.cols = 2
        self.part2 = GridLayout(cols=4, row_force_default=True, row_default_height=100,rows = 0)
    

        if os.path.isfile("prev_details.txt"):#Saves previous input to a txt file and redisplays it on launch
           with open("prev_details.txt", "r") as f:
            d = f.read().split(",")
            prev_preset = d[0]
            prev_time = d[1]

        else:
            prev_preset = ""
            prev_time = ""

        
        self.cols = 1

        self.logo = Image(source=('logo.png'))
        self.part1.add_widget(self.logo)

        self.part1.add_widget(Label(text=('')))

        self.part1.PresetL =Label(text=("Preset: " + prev_preset),font_size = 18)
        self.part1.add_widget(self.part1.PresetL)
        self.part1.Preset = CustomTextInput(text= (prev_preset),multiline=False)
        self.part1.add_widget(self.part1.Preset)
        
        self.part1.CycleTimeL = Label(text=("CycleTime Seconds: " + prev_time ),font_size = 18)
        self.part1.add_widget(self.part1.CycleTimeL)
        self.part1.CycleTime = CustomTextInput(text=(prev_time), multiline=False)
        self.part1.add_widget(self.part1.CycleTime)

        self.part1.Ct = Label(text=("Current Cycles: \n"),font_size = 18)
        self.part1.add_widget(self.part1.Ct)

        self.Apply = Button(text = "Apply",font_size = 40) 
        self.Apply.bind(on_press=self.Apply_Button)
        self.part1.add_widget(self.Apply)
        
        self.add_widget(self.part1)
######################################################################################

        self.Pause = Button(text=("Pause"),font_size = 40,size_hint_x=100, width=100)
        self.part2.add_widget(self.Pause)
        self.Pause.bind(on_press = self.Pause_Button)

        self.Reset = Button(text=("Reset"),font_size = 40,size_hint_x=100, width=100)
        self.part2.add_widget(self.Reset)
        self.Reset.bind(on_press = self.Reset_Button)


        self.part1.add_widget(self.part2)

    def Apply_Button(self, instance):
        GPIO.output(Relay1, GPIO.LOW)
        GPIO.output(Relay2, GPIO.LOW)
        GPIO.output(Relay3, GPIO.LOW)
        GPIO.output(Relay4, GPIO.LOW)

        self.part1.PresetG = self.part1.Preset.text#grabbing data from the fields to save
        self.part1.CycleTimeG = self.part1.CycleTime.text
        self.part1.cycles = 0
        self.part1.cycleCap = int(self.part1.PresetG)

        self.part1.PresetL.text = ("Preset: " + self.part1.PresetG)

        self.part1.CycleTimeL.text = ("CycleTime MiliSeconds: " + self.part1.CycleTimeG)
        self.user_input_timei = int(self.part1.CycleTimeG)
        self.user_input_timef = float(self.user_input_timei/1000)

        self.relay_wacker = float(self.user_input_timef/2)

        if self.cycle_count:
            self.cycle_count.cancel()
            self.cycle_count = None
        if self.relay_low:
            self.relay_low.cancel()
            self.relay_low = None 
  
            
        
        self.cycle_count = Clock.schedule_interval(self.cycle_updater, self.user_input_timef)
        self.relay_low = Clock.schedule_interval(self.relay_lowl, self.relay_wacker)
        
        with open("prev_details.txt", "w") as f:#Writing previous input to local txt file
            f.write(f"{self.part1.PresetG},{self.part1.CycleTimeG}")

    def cycle_updater(self, dt):
        self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.part1.cycleCap)
        self.part1.cycles += 1
        if(int(self.part1.cycles) == int(self.part1.cycleCap)):
            self.cycle_count.cancel()

    def Pause_Button(self,instance):
        if self.cycle_count:
            self.cycle_count.cancel()
            self.cycle_count = None

            self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.part1.cycleCap) + "\nPaused"
            self.Pause.text = "Resume"   
            print("PAUSED")         
        else:
            self.cycle_count = Clock.schedule_interval(self.cycle_updater, self.user_input_timef)
            self.Pause.text = "Pause"
            print("RESUME")

        if self.relay_low:
            self.relay_low.cancel()

        else:
            self.relay_low = Clock.schedule_interval(self.relay_lowl, self.relay_wacker)

           
    
    def relay_lowl(self, dt):
          if(self.relay_control == 0):
                GPIO.output(Relay1, GPIO.LOW)
                GPIO.output(Relay2, GPIO.LOW)
                GPIO.output(Relay3, GPIO.LOW)
                GPIO.output(Relay4, GPIO.LOW)
                print("Relay Low")
                self.relay_control += 1
          elif(self.relay_control == 1):
                GPIO.output(Relay1, GPIO.HIGH)
                GPIO.output(Relay2, GPIO.HIGH)
                GPIO.output(Relay3, GPIO.HIGH)
                GPIO.output(Relay4, GPIO.HIGH)
                print("relay_high")
                self.relay_control -= 1
 
    

        
    def Reset_Button(self,instance):
        GPIO.output(Relay1, GPIO.LOW)
        GPIO.output(Relay2, GPIO.LOW)
        GPIO.output(Relay3, GPIO.LOW)
        GPIO.output(Relay4, GPIO.LOW)

        self.part1.cycles = 0
        if self.cycle_count: 
            self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.part1.cycleCap)
        else:
            self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.part1.cycleCap) + "\nPaused"
            
"""class Keypad(GridLayout):
    def __init__(self, *args, **kwargs)
        self.cols = 3
        self.spacing = 10 
        self.createNums()
    def createNums(self):
        nums = [1,2,3,4,5,6,7,8,9,'<--','Enter']
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
