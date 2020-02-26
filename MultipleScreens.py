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

class Main_Menu(GridLayout):
    cycle_count = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3

        self.logo = Image(source=('logo.png'))
        self.add_widget(self.logo)

        self.add_widget(Label(text=('Main Menu'),font_size = 40))
    
        self.add_widget(Label(text=('')))
        self.add_widget(Label(text=('')))

        self.TaskManager = Button(text = "Task Manager",font_size = 30) 
        self.TaskManager.bind(on_press=self.Task_button)
        self.add_widget(self.TaskManager)
        
        self.add_widget(Label(text=('')))
        self.add_widget(Label(text=('')))

        self.TimeManager = Button(text = "Time Manager",font_size = 30)
        self.TimeManager.bind(on_press=self.Time_Button)
        self.add_widget(self.TimeManager)

        self.add_widget(Label(text=('')))
        self.add_widget(Label(text=('')))

        self.PresetManager = Button(text = "Preset Manager", font_size =30 )
        self.PresetManager.bind(on_press=self.Preset_Button)
        self.add_widget(self.PresetManager)

######################################################################################


    def Task_button(self, instance):
        pass
    def Time_Button(self, instance):
        pass
    def Preset_Button(self, instance):
        pass




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
            self._keyboard_closed, self,'text')
        if self._keyboard.widget:
            vkeyboard = self._keyboard.widget
            vkeyboard.layout = 'keynums.json'
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

        return Main_Menu()
        return MyKeyboardListener()

if __name__ =="__main__":
    GUI().run() 
