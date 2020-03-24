
import os
import time
import kivy
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
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
Window.fullscreen = True

class Main_Menu(Screen):
    cycle_count = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.part1 = GridLayout(cols=3, row_force_default=True, row_default_height=145,rows = 6,spacing = [4,4])

        self.logo = Image(source=('logo.png'))
        self.logo2 = Image(source=('logo.png'))
        self.logo3 = Image(source=('logo.png'))
        self.logo4 = Image(source=('logo.png'))
        self.logo5 = Image(source=('logo.png'))
        self.logo6 = Image(source=('logo.png'))
        self.logo7 = Image(source=('logo.png'))
        self.logo8 = Image(source=('logo.png'))

        self.part1.add_widget(self.logo)

        self.part1.add_widget(Label(text=('Main Menu'),font_size = 40))
    
        self.part1.add_widget(self.logo2)
        self.part1.add_widget(self.logo5)

        self.Relay_RunnerB = Button(text = "Relay Runner",font_size = 40) 
        self.Relay_RunnerB.bind(on_press=self.Relay_Runner_button)
        self.part1.add_widget(self.Relay_RunnerB)
        self.part1.add_widget(self.logo6)

        
        self.part1.add_widget(self.logo7)

        self.Relay_SettingsB = Button(text = "Relay Settings",font_size = 30)
        self.Relay_SettingsB.bind(on_press=self.Relay_Settings_Button)
        self.part1.add_widget(self.Relay_SettingsB)

        self.part1.add_widget(self.logo8)

        self.part1.add_widget(self.logo3)

    
        self.part1.add_widget(self.logo4)

        self.add_widget(self.part1)

    def Relay_Runner_button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'Relay_Runner' 
    def Relay_Settings_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'Relay_Settings' 

    
class Relay_Runner(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.part2 =  GridLayout(cols=3, row_force_default=True, row_default_height=100,rows = 6,spacing = [1,1])
        self.part2.add_widget(Label(text = "Task Settings"))
        self.MainMenu = Button(text = "Main Menu",font_size = 30)
        self.MainMenu.bind(on_press=self.Main_Menu_Button)
        self.part2.add_widget(self.MainMenu)
            
        self.add_widget(self.part2)

    def Main_Menu_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'menu'
class Relay_Settings(Screen):
    relay_current = 0
    r1p = 0
    r2p = 0
    r3p = 0
    r4p = 0

    r1r = 0
    r2r = 0
    r3r = 0 
    r4r = 0

    r1e = 0
    r2e = 0
    r3e = 0
    r4e = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.path.isfile("relay_data.txt"):#Saves previous input to a txt file and redisplays it on launch
            with open("relay_data.txt", "r") as f:
                d = f.read().split(",")
               
        self.part2 =  GridLayout(cols=3, row_force_default=True, row_default_height=100,rows = 6,spacing = [1,1])
        self.part3 =  GridLayout(cols=4, row_force_default=True, row_default_height=50,rows = 1,spacing = [1,1])

        self.part2.add_widget(Label(text = "Relay Settings"))
        self.MainMenu = Button(text = "Main Menu",font_size = 15)
        self.MainMenu.bind(on_press=self.Main_Menu_Button)
        self.part2.add_widget(self.MainMenu)

        self.Relay1_Button = Button(text = "Relay 1", font_size = 18)
        self.Relay1_Button.bind(on_press=self.Relay1_Press)
        self.part3.add_widget(self.Relay1_Button)
    
        self.Relay2_Button = Button(text = "Relay 2", font_size = 18)
        self.Relay2_Button.bind(on_press=self.Relay2_Press)
        self.part3.add_widget(self.Relay2_Button)

        self.Relay3_Button = Button(text = "Relay 3", font_size = 18)
        self.Relay3_Button.bind(on_press=self.Relay3_Press)
        self.part3.add_widget(self.Relay3_Button)

        self.Relay4_Button = Button(text = "Relay 4", font_size = 18)
        self.Relay4_Button.bind(on_press=self.Relay4_Press)
        self.part3.add_widget(self.Relay4_Button)
        self.part2.add_widget(Label(text = ""))

        self.part2.add_widget(self.part3)
        self.current_relay = Label(text = "Current Relay:")
        self.part2.add_widget(self.current_relay)

        self.part2.add_widget(Label(text = ""))


        self.preset = Label(text="Preset: ",font_size = 18)
        self.part2.add_widget(self.preset)
        
        self.presetI = CustomTextInput(multiline=False,font_size = 18)
        self.part2.add_widget(self.presetI)
        
        self.part2.add_widget(Label(text = ""))

        self.retract_time = Label(text = "Retract Time: ")
        self.part2.add_widget(self.retract_time)

        self.retract_timeI = CustomTextInput(multiline = False,font_size = 18)
        self.part2.add_widget(self.retract_timeI)

        self.part2.add_widget(Label(text = ""))

        self.extend_time = Label(text = "Extend Time: ")
        self.part2.add_widget(self.extend_time)

        self.extend_timeI = CustomTextInput(multiline = False,font_size = 18)
        self.part2.add_widget(self.extend_timeI)

        self.submitB = Button(text = "SUBMIT",font_size = 18)
        self.submitB.bind(on_press =self.Submit)
        self.part2.add_widget(self.submitB)
        self.add_widget(self.part2)


    def Relay1_Press(self, instance):
        self.current_relay.text = "Current Relay: Relay 1"
        self.relay_current = 1
    def Relay2_Press(self, instance):
        self.relay_current = 2
        self.current_relay.text = "Current Relay: Relay 2"
    def Relay3_Press(self, instance):
        self.relay_current = 3
        self.current_relay.text = "Current Relay: Relay 3"
    def Relay4_Press(self, instance):
        self.relay_current = 4
        self.current_relay.text = "Current Relay: Relay 4"

    def Submit(self,instance):
        if(self.current_relay == 1):
            self.r1p = int(self.presetI.txt)
            self.r1r = int(self.retract_timeI.txt)
            self.r1e = int(self.extend_timeI.txt)

            self.sr1p = str(self.r1p)
            self.sr1r = str(self.r1r)
            self.sr1e = str(self.r1e)
            
            with open("relay_data.txt", "w") as f:#Writing previous input to local txt file
                f.write(f"{self.r1p},{self.r1r},{self.r1e}")
            print(self.r1p,self.r1r,self.r1e)

    def Main_Menu_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'menu'

class CustomTextInput(TextInput):
    def on_keyboard(self, instance, value):
        if self.keyboard.widget:
            vkeyboard = self.keyboard.widget
            vkeyboard.layout = 'keynums.json'
class GUI(App):
    def build(self):
        self.sm = ScreenManager() 
        self.sm.add_widget(Main_Menu(name='menu'))
        self.sm.add_widget(Relay_Runner(name = 'Relay_Runner'))
        self.sm.add_widget(Relay_Settings(name = 'Relay_Settings'))

        return self.sm
    
    
if __name__ =="__main__":
    GUI().run() 
