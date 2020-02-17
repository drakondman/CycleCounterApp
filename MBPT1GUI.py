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

GPIO.output(Relay1, GPIO.LOW)
GPIO.output(Relay2, GPIO.LOW)
GPIO.output(Relay3, GPIO.LOW)
GPIO.output(Relay4, GPIO.LOW)

class Interact(GridLayout):

    tooFastArray = []
    for i in range(-1,100):
        tooFastArray.append(str(i))


    cycle_count = None
    relay_low = None
    relay_howl = None
    relay_control = 0
    user_input_timef = 0
    cycleCap = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.part1 = GridLayout()
        self.part1.cols = 2
        self.part2 = GridLayout(cols=4, row_force_default=True, row_default_height=65,rows = 2)
    

        if os.path.isfile("prev_details.txt"):#Saves previous input to a txt file and redisplays it on launch
           with open("prev_details.txt", "r") as f:
            d = f.read().split(",")
            prev_preset = d[0]
            prev_time = d[1]

        else:
            prev_preset = ""
            prev_time = ""

        self.logo = Image(source=('logo.png'))
        self.part1.add_widget(self.logo)

        self.part1.add_widget(Label(text=('')))

        self.part1.PresetL =Label(text=("Preset:\n" + prev_preset),font_size = 18)
        self.part1.add_widget(self.part1.PresetL)
        self.part1.Preset = CustomTextInput(text= (prev_preset),multiline=False,height = 40, background_color = [1,1,1,.95] )
        self.part1.add_widget(self.part1.Preset)
        
        self.part1.CycleTimeL = Label(text=("CycleTime Miliseconds:\n" + prev_time),font_size = 18,height = 40)
        self.part1.add_widget(self.part1.CycleTimeL)
        self.part1.CycleTime = CustomTextInput(text=(prev_time), multiline=False, background_color = [1,1,1,.95])
        self.part1.add_widget(self.part1.CycleTime)

        self.part1.Ct = Label(text=("Current Cycles:\n"),font_size = 18)
        self.part1.add_widget(self.part1.Ct)

        self.Apply = Button(text = "Apply",font_size = 40) 
        self.Apply.bind(on_press=self.Apply_Button)
        self.part1.add_widget(self.Apply)
        
        self.add_widget(self.part1)

        self.Pause = Button(text=("Pause"),font_size = 25,size_hint_x=10, width=100,height=40)
        self.part2.add_widget(self.Pause)
        self.Pause.bind(on_press = self.Pause_Button)

        self.Reset = Button(text=("Reset"),font_size = 25,size_hint_x=10, width=100,height=40)
        self.part2.add_widget(self.Reset)
        self.Reset.bind(on_press = self.Reset_Button)
        self.part2.add_widget(Label(text=('')))
        self.part2.add_widget(Label(text=('')))
    
        



        self.part1.add_widget(self.part2)

    def Apply_Button(self, instance):
        self.part1.PresetG = self.part1.Preset.text#grabbing data from the fields to save
        self.part1.CycleTimeG = self.part1.CycleTime.text

        if (self.part1.PresetG == ''):
            print("No fields Full Preset")
        elif(self.part1.CycleTimeG == ''):
            print("No fields Full Cycle Time")
        elif(self.part1.CycleTimeG in self.tooFastArray):
            print("Too Fast Slow Down")
        elif(self.part1.PresetG == '0'):
            print("sorry but 0 is not vaild")
        else:
            self.user_input_timei = int(self.part1.CycleTimeG)
            self.cycleCap = int(self.part1.PresetG)
            if(self.cycleCap >= 9999999999999):
                print("Too Big Preset")
            elif(self.user_input_timei >= 999999):
                print("Too Big Time")
            else:
                self.part1.cycles = 0

                self.part1.PresetL.text = ("Preset:\n" + self.part1.PresetG)

                self.part1.CycleTimeL.text = ("CycleTime Miliseconds:\n" + self.part1.CycleTimeG)

                self.user_input_timef = float(self.user_input_timei/1000)
                self.relay_wacker = float(self.user_input_timef/2)

                if self.cycle_count:
                    self.cycle_count.cancel()
                    self.cycle_count = None
                if self.relay_low:
                    self.relay_low.cancel()
                
                self.cycle_count = Clock.schedule_interval(self.cycle_updater, self.user_input_timef)
                self.relay_low = Clock.schedule_interval(self.relay_lowl, self.relay_wacker)
            

                with open("prev_details.txt", "w") as f:#Writing previous input to local txt file
                    f.write(f"{self.part1.PresetG},{self.part1.CycleTimeG}")

    def cycle_updater(self, dt):

        self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.cycleCap)
        self.part1.cycles += 1
        if(int(self.part1.cycles) == int(self.cycleCap)):
            self.cycle_count.cancel()
  
    def relay_lowl(self, dt):
         
        if(self.relay_control == 0):
                print("Relay Low")
                GPIO.output(Relay1, GPIO.LOW)
                GPIO.output(Relay2, GPIO.LOW)
                GPIO.output(Relay3, GPIO.LOW)
                GPIO.output(Relay4, GPIO.LOW)
                self.relay_control += 1
        elif(self.relay_control == 1):
                print("relay_high")
                GPIO.output(Relay1, GPIO.HIGH)
                GPIO.output(Relay2, GPIO.HIGH)
                GPIO.output(Relay3, GPIO.HIGH)
                GPIO.output(Relay4, GPIO.HIGH)                
                self.relay_control -= 1
    
    def Pause_Button(self,instance):
        if(self.user_input_timef == 0):
            print("Nope")
        else:
            if self.cycle_count:
                self.cycle_count.cancel()
                self.cycle_count = None

                self.part1.Ct.text = "Current Cycles: " + str(self.part1.cycles) + "\nPreset: " + str(self.cycleCap) + "\nPaused"
                GPIO.output(Relay1, GPIO.LOW)
                GPIO.output(Relay2, GPIO.LOW)
                GPIO.output(Relay3, GPIO.LOW)
                GPIO.output(Relay4, GPIO.LOW)                
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
