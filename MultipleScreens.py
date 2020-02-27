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

        self.part1 = GridLayout(cols=3, row_force_default=True, row_default_height=150,rows = 6,spacing = [4,4])

        self.logo = Image(source=('logo.png'))
        self.part1.add_widget(self.logo)

        self.part1.add_widget(Label(text=('Main Menu'),font_size = 40))
    
        self.part1.add_widget(Label(text=('')))
        self.part1.add_widget(Label(text=('')))

        self.TaskManager = Button(text = "Task Manager",font_size = 40) 
        self.TaskManager.bind(on_press=self.Task_button)
        self.part1.add_widget(self.TaskManager)
        
        self.part1.add_widget(Label(text=('')))
        self.part1.add_widget(Label(text=('')))

        self.TaskSettingsB = Button(text = "Task Settings",font_size = 30)
        self.TaskSettingsB.bind(on_press=self.Task_Settings_Button)
        self.part1.add_widget(self.TaskSettingsB)

        self.part1.add_widget(Label(text=('')))
        self.part1.add_widget(Label(text=('')))

        self.CalibrationScreenB = Button(text = "Calibration Screen", font_size =30 )
        self.CalibrationScreenB.bind(on_press=self.Calibration_Screen_Button)
        self.part1.add_widget(self.CalibrationScreenB)
        
        self.add_widget(self.part1)

    def Task_button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'task_manager' 
    def Task_Settings_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'task_settings' 

    def Calibration_Screen_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'calibration_screen' 

class Task_Manager(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.part2 =  GridLayout(cols=3, row_force_default=False, row_default_height=100,spacing = [1,2], width = 100)
        self.part4 = GridLayout(cols =2,  row_force_default=True, row_default_height=50,spacing = [1,1], width = 50)
        self.part3 = GridLayout(cols =2,  row_force_default=True, row_default_height=60,spacing = [1,1], width = 50)
        self.part5 = GridLayout(cols =1,  row_force_default=True, row_default_height=50,spacing = [1,1], width = 50)
        self.part6 = GridLayout(cols =1,  row_force_default=True, row_default_height=75,spacing = [2,2], width = 75)
        self.part7 = GridLayout(cols =2,  row_force_default=True, row_default_height=18,spacing = [1,1], width = 50)
        self.part8 = GridLayout(cols =3,  row_force_default=True, row_default_height=60,spacing = [1,1], col_default_width = 150)
        self.part9 = GridLayout(cols =1,  row_force_default=True, row_default_height=60,spacing = [1,1], col_default_width = 150)

        self.logo = Image(source=('logo.png'),width = 200, height = 200)
        self.part2.add_widget(self.logo)

        self.part4.add_widget(Label(text = "Cycle Preset:", font_size = 18))
        self.Cycle_Preset = Label(text = "00000000000")
        self.part4.add_widget(self.Cycle_Preset) 
        self.part4.add_widget(Label(text = "Pause every\n # of cycles",font_size = 12))
        self.Cycle_Pause = Label(text = "0000000000")
        self.part4.add_widget(self.Cycle_Pause)
        
        self.part5.add_widget(Label(text = "Cycle Counter",font_size = 18))
        self.Current_CyclesL = Label(text = "0000000000", font_size = 18)
        self.part7.add_widget(Label(text = " Current Cycles:"))
        self.part7.add_widget(self.Current_CyclesL)
        self.part5.add_widget(self.part7)

        self.part6.add_widget(self.part4)
        self.part6.add_widget(self.part5)

        self.part2.add_widget(self.part6)

        self.reset = Button(text = "Reset", font_size = 18, background_color = [1,0,0,1], color = [0,0,0,1])
        self.reset.bind(on_press = self.Reset)
        self.part3.add_widget(self.reset)

        self.start = Button(text = "Start", font_size = 18, background_color = [0,1,0,1],color = [0,0,0,1] )
        self.start.bind(on_press = self.Start)
        self.part3.add_widget(self.start)

        self.part3.add_widget(Label(text = ""))

        self.pause = Button(text = "Pause", font_size = 18, background_color = [1,0,0,1], color = [0,0,0,1])
        self.pause.bind(on_press = self.Pause)
        self.part3.add_widget(self.pause)

        self.part2.add_widget(self.part3)
        self.part2.add_widget(Label(text = ""))

        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))

        self.sendhome = Button(text = "Send Back Home", font_size = 18, background_color = [1,0,0,1], color = [0,0,0,1],width = 50, height = 50)
        self.pause.bind(on_press = self.Send_Home)
        self.part9.add_widget(self.sendhome) 
        self.part2.add_widget(self.part9)    

      
        self.TaskSettingsB = Button(text = "Task Settings",font_size = 18)
        self.TaskSettingsB.bind(on_press=self.Task_Settings_Button)
        self.part8.add_widget(self.TaskSettingsB)
    
        self.CalibrationScreenB = Button(text = "Calibration Screen", font_size =18 )
        self.CalibrationScreenB.bind(on_press=self.Calibration_Screen_Button)
        self.part8.add_widget(self.CalibrationScreenB)

        self.MainMenu = Button(text = "Main Menu",font_size = 18 )
        self.MainMenu.bind(on_press=self.Main_Menu_Button)
        self.part8.add_widget(self.MainMenu)

        self.part2.add_widget(self.part8)

        
        self.add_widget(self.part2)

    def Reset(self, instance):
        pass 

    def Start(self, instance): 
        pass 

    def Pause(self, instance):
        pass

    def Send_Home(self, instance):
        pass

    def Task_Settings_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'task_settings' 

    def Calibration_Screen_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'calibration_screen' 


    def Main_Menu_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'menu'

class Task_Settings(Screen):
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

class Calibration_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.part2 =  GridLayout(cols=3, row_force_default=True, row_default_height=100,rows = 6,spacing = [1,1])
        self.part2.add_widget(Label(text = "Calibration Settings"))
        self.MainMenu = Button(text = "Main Menu",font_size = 30)
        self.MainMenu.bind(on_press=self.Main_Menu_Button)
        self.part2.add_widget(self.MainMenu)
            
        self.add_widget(self.part2)

    def Main_Menu_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'menu'




class GUI(App):
    def build(self):
        self.sm = ScreenManager() 
        self.sm.add_widget(Main_Menu(name='menu'))
        self.sm.add_widget(Task_Manager(name = 'task_manager'))
        self.sm.add_widget(Task_Settings(name = 'task_settings'))
        self.sm.add_widget(Calibration_Screen(name = 'calibration_screen'))

        return self.sm
    
    
if __name__ =="__main__":
    GUI().run() 
