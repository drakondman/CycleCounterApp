import os
import time
import kivy
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
class Interact(GridLayout):
    cycle_count = None

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
        self.part1.Preset = TextInput(text= (prev_preset),multiline=False)
        self.part1.add_widget(self.part1.Preset)
        
        self.part1.CycleTimeL = Label(text=("CycleTime Seconds: " + prev_time ),font_size = 18)
        self.part1.add_widget(self.part1.CycleTimeL)
        self.part1.CycleTime = TextInput(text=(prev_time), multiline=False)
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

        self.part1.PresetG = self.part1.Preset.text#grabbing data from the fields to save
        self.part1.CycleTimeG = self.part1.CycleTime.text
        self.part1.cycles = 0
        self.part1.cycleCap = int(self.part1.PresetG)

        self.part1.PresetL.text = ("Preset: " + self.part1.PresetG)

        self.part1.CycleTimeL.text = ("CycleTime Seconds: " + self.part1.CycleTimeG)
        self.user_input_time = int(self.part1.CycleTimeG)
        if self.cycle_count:
            self.cycle_count.cancel()
            self.cycle_count = None
        
        self.cycle_count = Clock.schedule_interval(self.cycle_updater, self.user_input_time)

        with open("prev_details.txt", "w") as f:#Writing previous input to local txt file
            f.write(f"{self.part1.PresetG},{self.part1.CycleTimeG}")

    def cycle_updater(self, dt):
        print('hit clock')

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
        else:
            self.cycle_count = Clock.schedule_interval(self.cycle_updater, self.user_input_time)
            self.Pause.text = "Pause"
   
    def Reset_Button(self,instance):
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
class MyKeyboardListener(Widget):

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

class GUI(App):
    def build(self):
        return Interact()
if __name__ =="__main__":
    GUI().run() 
    GUI(MyKeyboardListener())
