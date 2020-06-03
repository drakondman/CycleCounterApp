import os
import time
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
#Window.fullscreen = True

"""GPIO.setwarnings(False)

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
GPIO.output(Relay4, GPIO.LOW)"""


class Main_Menu(Screen):#Class that displays the main menu screen
    cycle_count = None
    def __init__(self, **kwargs):#inital Main screen graphics
        super().__init__(**kwargs)
        self.part1 = GridLayout(cols=3, row_force_default=True, row_default_height=145,rows = 6,spacing = [4,4])#Setting the Gridlayout and paramaters
        self.logo = Image(source=('logo.png'))
        self.part1.add_widget(self.logo)
        self.part1.add_widget(Label(text=('Main Menu'),font_size = 40))
        self.part1.add_widget(Label(text="")) #Blank Label acts as a empty box in the gridlayout
        self.part1.add_widget(Label(text=""))
        self.Relay_RunnerB = Button(text = "Relay Runner",font_size = 40) 
        self.Relay_RunnerB.bind(on_press=self.Relay_Runner_button)
        self.part1.add_widget(self.Relay_RunnerB)
        self.part1.add_widget(Label(text=""))
        self.part1.add_widget(Label(text=""))
        self.Relay_SettingsB = Button(text = "Relay Settings",font_size = 18)
        self.Relay_SettingsB.bind(on_press=self.Relay_Settings_Button)
        self.part1.add_widget(self.Relay_SettingsB)
        self.part1.add_widget(Label(text=""))
        self.part1.add_widget(Label(text=""))
        self.part1.add_widget(Label(text=""))
        self.add_widget(self.part1)
    def Relay_Runner_button(self, instance): #Function for Screen change button
        app = App.get_running_app()
        app.sm.current = 'Relay_Runner' 
    def Relay_Settings_Button(self, instance):#Fuction for Screen Change Button
        app = App.get_running_app()
        app.sm.current = 'Relay_Settings' 
class Relay_Runner(Screen):#Class for the screen that runs the relays
    r1p = ""#varibles from the relay settings page that control the times and presets
    r1r = ""
    r1e = ""
    r2p = ""
    r2r = ""
    r2e = ""
    r3p = ""
    r3r = "" 
    r3e = ""
    r4p = ""
    r4r = ""
    r4e = ""
    mrec1 = 0
    mrec2 = 0 
    mrec3 = 0
    mrec4 = 0
    relay_Mcontroller1 = None
    relay_Mcontroller2 = None
    relay_Mcontroller3 = None
    relay_Mcontroller4 = None
    cycleCap1 = 0
    cycleCap2 = 0
    cycleCap3 = 0
    cycleCap4 = 0
    cycles1 = 0
    cycles2 = 0
    cycles3 = 0
    cycles4 = 0
    etg1 = 0.0
    etg2 = 0.0
    etg3 = 0.0
    etg4 = 0.0
    rtg1 = 0.0
    rtg2 = 0.0
    rtg3 = 0.0
    rtg4 = 0.0
    cg1 = .00001
    cg2 = .00001
    cg3 = .00001
    cg4 = .00001
    r1rc1 = 0.0
    r1rc2 = 0.0
    r1rc3 = 0.0
    r2rc1 = 0.0
    r2rc2 = 0.0
    r2rc3 = 0.0
    r3rc1 = 0.0
    r3rc2 = 0.0
    r3rc3 = 0.0
    r4rc1 = 0.0
    r4rc2 = 0.0
    r4rc3 = 0.0
    r1rcM = 0
    r2rcM = 0
    r3rcM = 0
    r4rcM = 0
    sC1 = False
    sC2 = False
    sC3 = False
    sC4 = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.path.isfile("relay_data.txt"):#Saves previous input to a txt file and redisplays it on launch
            with open("relay_data.txt", "r") as f:
                d = f.read().split(",")
                self.r1p = d[0]
                self.r1r = d[1]
                self.r1e = d[2]
                self.r2p = d[3]
                self.r2r = d[4]
                self.r2e = d[5]
                self.r3p = d[6]
                self.r3r = d[7]
                self.r3e = d[8]
                self.r4p = d[9]
                self.r4r = d[10]
                self.r4e = d[11]
                f.flush()
                f.close()
        else:
            self.r1p = ""
            self.r1r = ""
            self.r1e = ""
            self.r2p = ""
            self.r2r = ""
            self.r2e = ""
            self.r3p = ""
            self.r3r = ""
            self.r3e = ""
            self.r4p = ""
            self.r4r = ""
            self.r4e = ""
        self.part2 =  GridLayout(cols=4, row_force_default=True, row_default_height=100,rows = 8) #Setting Main grid and subgrid layouts for the task run screen
        self.part3 =  GridLayout(cols=1, row_force_default=True, row_default_height=25)
        self.part4 =  GridLayout(cols=1, row_force_default=True, row_default_height=25)
        self.part5 =  GridLayout(cols=1, row_force_default=True, row_default_height=25)
        self.part6 =  GridLayout(cols=1, row_force_default=True, row_default_height=25)
        self.part7 =  GridLayout(cols=2, row_force_default=True, row_default_height=20,rows = 2)
        self.part8 =  GridLayout(cols=2, row_force_default=True, row_default_height=20,rows = 2)
        self.part9 =  GridLayout(cols=2, row_force_default=True, row_default_height=20,rows = 2)
        self.part10 =  GridLayout(cols=2, row_force_default=True, row_default_height=20,rows = 2)
        self.logo = Image(source=('logo.png'))
        self.part2.add_widget(self.logo)
        self.part2.add_widget(Label(text = "Task Runner"))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part3.add_widget(Label(text = "Relay 1"))
        self.part3.add_widget(Label(text = ("Preset: " + self.r1p)))
        self.part3.add_widget(Label(text = ("Extend Time: " + self.r1e)))
        self.part3.add_widget(Label(text = ("Retract Time: " + self.r1r)))
        self.mer1 = Button(text = "Manual Extend")
        self.mer1.bind(on_press = self.r1mer)
        self.part3.add_widget(self.mer1)
        self.r1c = Label(text = "Current Cycles: ")
        self.part3.add_widget(self.r1c)
        self.r1pause = Button(text = "Pause", background_color = [1,0,0,1], color = [0,0,0,1])
        self.r1pause.bind(on_press = self.r1Pause)
        self.part7.add_widget(self.r1pause)
        self.r1reset = Button(text = "Reset", background_color = [1,0,0,1], color = [0,0,0,1])
        self.r1reset.bind(on_press = self.r1Reset,)
        self.part7.add_widget(self.r1reset)
        self.r1start = Button(text = "Start", background_color = [0,1,0,1],color = [0,0,0,1])
        self.r1start.bind(on_press = self.r1Start)
        self.part7.add_widget(self.r1start)
        self.part3.add_widget(self.part7)
        self.part2.add_widget(self.part3)
        self.part4.add_widget(Label(text = "Relay 2"))
        self.part4.add_widget(Label(text = ("Preset: " + self.r2p)))
        self.part4.add_widget(Label(text = ("Extend Time: " + self.r2e)))
        self.part4.add_widget(Label(text = ("Retract Time: " + self.r2r)))
        self.mer2 = Button(text = "Manual Extend")
        self.mer2.bind(on_press = self.r2mer)
        self.part4.add_widget(self.mer2)
        self.r2c = Label(text = "Current Cycles: ")
        self.part4.add_widget(self.r2c)
        self.r2pause = Button(text = "Pause", background_color = [1,0,0,1], color = [0,0,0,1])
        self.r2pause.bind(on_press = self.r2Pause)
        self.part8.add_widget(self.r2pause)
        self.r2reset = Button(text = "Reset", background_color = [1,0,0,1], color = [0,0,0,1])
        self.r2reset.bind(on_press = self.r2Reset)
        self.part8.add_widget(self.r2reset)
        self.r2start = Button(text = "Start", background_color = [0,1,0,1],color = [0,0,0,1])
        self.r2start.bind(on_press = self.r2Start)
        self.part8.add_widget(self.r2start)
        self.part4.add_widget(self.part8)
        self.part2.add_widget(self.part4)
        self.part5.add_widget(Label(text = "Relay 3"))
        self.part5.add_widget(Label(text = ("Preset: " + self.r3p)))
        self.part5.add_widget(Label(text = ("Extend Time: " + self.r3e)))
        self.part5.add_widget(Label(text = ("Retract Time: " + self.r3r)))
        self.mer3 = Button(text = "Manual Extend")
        self.mer3.bind(on_press = self.r3mer)
        self.part5.add_widget(self.mer3)
        self.r3c = Label(text = "Current Cycles: ")
        self.part5.add_widget(self.r3c)
        self.r3pause = Button(text = "Pause", background_color = [1,0,0,1], color = [0,0,0,1])
        self.r3pause.bind(on_press = self.r3Pause)
        self.part9.add_widget(self.r3pause)
        self.r3reset = Button(text = "Reset", background_color = [1,0,0,1], color = [0,0,0,1])
        self.r3reset.bind(on_press = self.r3Reset)
        self.part9.add_widget(self.r3reset)
        self.r3start = Button(text = "Start", background_color = [0,1,0,1],color = [0,0,0,1])
        self.r3start.bind(on_press = self.r3Start)
        self.part9.add_widget(self.r3start)
        self.part5.add_widget(self.part9)
        self.part2.add_widget(self.part5)
        self.part6.add_widget(Label(text = "Relay 4"))
        self.part6.add_widget(Label(text = ("Preset: " + self.r4p)))
        self.part6.add_widget(Label(text = ("Extend Time: " + self.r4e)))
        self.part6.add_widget(Label(text = ("Retract Time: " + self.r4r)))
        self.mer4 = Button(text = "Manual Extend")
        self.mer4.bind(on_press = self.r4mer)
        self.part6.add_widget(self.mer4)
        self.r4c = Label(text = "Current Cycles: ")
        self.part6.add_widget(self.r4c)
        self.r4pause = Button(text = "Pause", background_color = [1,0,0,1], color = [0,0,0,1])
        self.r4pause.bind(on_press = self.r4Pause)
        self.part10.add_widget(self.r4pause)
        self.r4reset = Button(text = "Reset", background_color = [1,0,0,1], color = [0,0,0,1])
        self.r4reset.bind(on_press = self.r4Reset)
        self.part10.add_widget(self.r4reset)
        self.r4start = Button(text = "Start", background_color = [0,1,0,1],color = [0,0,0,1])
        self.r4start.bind(on_press = self.r4Start)
        self.part10.add_widget(self.r4start)
        self.part6.add_widget(self.part10)
        self.part2.add_widget(self.part6)
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.part2.add_widget(Label(text = ""))
        self.MainMenu = Button(text = "Main Menu",font_size = 15)# Screen Switch Button
        self.MainMenu.bind(on_press=self.Main_Menu_Button)
        self.part2.add_widget(self.MainMenu)
        self.RelaySettingsB = Button(text = "Relay Settings",font_size = 15)# Screen Switch Button
        self.RelaySettingsB.bind(on_press=self.Relay_Settings_Button)
        self.part2.add_widget(self.RelaySettingsB)     
        self.add_widget(self.part2)
    def r1mer(self,instance):
        if(self.mrec1 == 0):
            print("Manual Extend")
            self.mer1.text = "Manual Retract"
            self.mrec1 += 1
            #GPIO.output(Relay1, GPIO.HIGH)

        else: 
            print("Manual Retract")
            self.mer1.text = "Manual Extend"
            self.mrec1 -= 1
            #GPIO.output(Relay1, GPIO.LOW)

    def r2mer(self,instance):
        if(self.mrec2 == 0):
            print("Manual Extend")
            self.mer2.text = "Manual Retract"
            self.mrec2 += 1
            #GPIO.output(Relay2, GPIO.HIGH)
        else: 
            print("Manual Retract")
            self.mer2.text = "Manual Extend"
            self.mrec2 -= 1
            #GPIO.output(Relay2, GPIO.LOW)
    def r3mer(self,instance):
        if(self.mrec3 == 0):
            print("Manual Extend")
            self.mer3.text = "Manual Retract"
            self.mrec3 += 1
            #GPIO.output(Relay3, GPIO.HIGH)
        else: 
            print("Manual Retract")
            self.mer3.text = "Manual Extend"
            self.mrec3 -= 1
            #GPIO.output(Relay3, GPIO.LOW)

    def r4mer(self,instance):
        if(self.mrec4 == 0):
            print("Manual Extend")
            self.mer4.text = "Manual Retract"
            self.mrec4 += 1
            #GPIO.output(Relay4, GPIO.HIGH)
        else: 
            print("Manual Retract")
            self.mer4.text = "Manual Extend"
            self.mrec4 -= 1
            #GPIO.output(Relay4, GPIO.LOW)
#####################################

    def r1Start(self,instance):
        if self.relay_Mcontroller1:
            self.relay_Mcontroller1.cancel()
        self.cycles1 = 0

        self.r1ecc = int(self.r1e)
        self.r1rcc = int(self.r1r)

        self.cycleCap1 = int(self.r1p)

        self.etg1 = float(self.r1ecc/1000)
        self.rtg1 = float(self.r1rcc/1000)
        self.sC1 = True
        self.relay_Mcontroller1 = Clock.schedule_interval(self.relay_controller1,self.cg1)

    def r1Pause(self, instance):
        #GPIO.output(Relay1, GPIO.LOW)
        if(self.sC1 == False):
            print("Nope")
        else:
            if self.relay_Mcontroller1:
                self.relay_Mcontroller1.cancel()
                self.relay_Mcontroller1 = None

                self.r1pause.text = "Resume"   
                print("PAUSED")         
            else:
                self.relay_Mcontroller1 = Clock.schedule_interval(self.relay_controller1,self.cg1)
                self.r1pause.text = "Pause"
                print("RESUME")

    def r1Reset(self,instance):
        if(self.cycleCap1 == 0):
            print("NO RESET")
        else:
            self.cycles1 = 0
            print("RESETED")
            self.r1c.text = ("Current Cycles: " + str(self.cycles1))

    def relay_controller1(self,dt):
        if(self.r1rcM == 0):
            self.r1rc1 += 0.01
            if(self.r1rc1 <= self.etg1):
                print("Current Extend")
                #GPIO.output(Relay1, GPIO.HIGH)
            else:
                print("switching")
                self.r1rcM += 1
                self.r1rc1 = 0.0
        elif(self.r1rcM == 1):
            self.r1rc2 += 0.01
            if(self.r1rc2 <= self.rtg1):
                print("Current Retract")
                #GPIO.output(Relay1, GPIO.LOW)
            else:
                print("switching")
                self.r1rcM += 1
                self.r1rc2 = 0.0 
        elif(self.r1rcM == 2):
            self.cycles1 += 1    
            if(self.cycles1 >= self.cycleCap1):
                print("Stopped")
                print(self.cycleCap1)
                self.relay_Mcontroller1.cancel()
                #GPIO.output(Relay1, GPIO.LOW)

            else:
                self.r1c.text = "Current Cycles: " + str(self.cycles1)         
                self.r1rcM -= 2
                print("Completed 1 Cycle")
#######################################

    def r2Start(self,instance):
        if self.relay_Mcontroller2:
            self.relay_Mcontroller2.cancel()
        self.cycles2 = 0

        self.r2ecc = int(self.r2e)
        self.r2rcc = int(self.r2r)

        self.cycleCap2 = int(self.r2p)

        self.etg2 = float(self.r2ecc/1000)
        self.rtg2 = float(self.r2rcc/1000)
        self.sC2 = True
        self.relay_Mcontroller2 = Clock.schedule_interval(self.relay_controller2,self.cg2)


    def r2Pause(self, instance):
        #GPIO.output(Relay1, GPIO.LOW)
        if(self.sC2 == False):
            print("Nope")
        else:
            if self.relay_Mcontroller2:
                self.relay_Mcontroller2.cancel()
                self.relay_Mcontroller2 = None

                self.r2pause.text = "Resume"   
                print("PAUSED")         
            else:
                self.relay_Mcontroller2 = Clock.schedule_interval(self.relay_controller2,self.cg2)
                self.r2pause.text = "Pause"
                print("RESUME")


    def r2Reset(self,instance):
        if(self.cycleCap2 == 0):
            print("NO RESET")
        else:
            self.cycles2 = 0
            print("RESETED")
            self.r2c.text = ("Current Cycles: " + str(self.cycles2))


    def relay_controller2(self,dt):
        if(self.r2rcM == 0):
            self.r2rc1 += 0.01
            if(self.r2rc1 <= self.etg2):
                print("Current Extend")
                #GPIO.output(Relay2, GPIO.HIGH)
            else:
                print("switching")
                self.r2rcM += 1
                self.r2rc1 = 0.0
        elif(self.r2rcM == 1):
            self.r2rc2 += 0.01
            if(self.r2rc2 <= self.rtg2):
                print("Current Retract")
                #GPIO.output(Relay2, GPIO.LOW)
            else:
                print("switching")
                self.r2rcM += 1
                self.r2rc2 = 0.0 
        elif(self.r2rcM == 2):
            self.cycles2 += 1    
            if(self.cycles2 >= self.cycleCap2):
                print("Stopped")
                print(self.cycleCap2)
                self.relay_Mcontroller2.cancel()
                #GPIO.output(Relay2, GPIO.LOW)

            else:
                self.r2c.text = "Current Cycles: " + str(self.cycles2)         
                self.r2rcM -= 2
                print("Completed 1 Cycle")
#######################################

    def r3Start(self,instance):
        if self.relay_Mcontroller3:
            self.relay_Mcontroller3.cancel()
        self.cycles3 = 0

        self.r3ecc = int(self.r3e)
        self.r3rcc = int(self.r3r)

        self.cycleCap3 = int(self.r3p)

        self.etg3 = float(self.r3ecc/1000)
        self.rtg3 = float(self.r3rcc/1000)
        self.sC3 = True
        self.relay_Mcontroller3 = Clock.schedule_interval(self.relay_controller3,self.cg3)

    def r3Pause(self, instance):
        #GPIO.output(Relay3, GPIO.LOW)
        if(self.sC3 == False):
            print("Nope")
        else:
            if self.relay_Mcontroller3:
                self.relay_Mcontroller3.cancel()
                self.relay_Mcontroller3 = None

                self.r3pause.text = "Resume"   
                print("PAUSED")         
            else:
                self.relay_Mcontroller3 = Clock.schedule_interval(self.relay_controller3,self.cg3)
                self.r3pause.text = "Pause"
                print("RESUME")

    def r3Reset(self,instance):
        if(self.cycleCap3 == 0):
            print("NO RESET")
        else:
            self.cycles3 = 0
            print("RESETED")
            self.r3c.text = ("Current Cycles: " + str(self.cycles3))

    def relay_controller3(self,dt):
        if(self.r3rcM == 0):
            self.r3rc1 += 0.01
            if(self.r3rc1 <= self.etg3):
                print("Current Extend")
                #GPIO.output(Relay3, GPIO.HIGH)
            else:
                print("switching")
                self.r3rcM += 1
                self.r3rc1 = 0.0
        elif(self.r3rcM == 1):
            self.r3rc2 += 0.01
            if(self.r3rc2 <= self.rtg3):
                print("Current Retract")
                #GPIO.output(Relay3, GPIO.LOW)
            else:
                print("switching")
                self.r3rcM += 1
                self.r3rc2 = 0.0 
        elif(self.r3rcM == 2):
            self.cycles3 += 1    
            if(self.cycles3 >= self.cycleCap3):
                print("Stopped")
                print(self.cycleCap3)
                self.relay_Mcontroller3.cancel()
                #GPIO.output(Relay3, GPIO.LOW)

            else:
                self.r3c.text = "Current Cycles: " + str(self.cycles3)         
                self.r3rcM -= 2
                print("Completed 1 Cycle")
#######################################

    def r4Start(self,instance):
        if self.relay_Mcontroller4:
            self.relay_Mcontroller4.cancel()
        self.cycles4 = 0

        self.r4ecc = int(self.r4e)
        self.r4rcc = int(self.r4r)

        self.cycleCap4 = int(self.r4p)

        self.etg4 = float(self.r4ecc/1000)
        self.rtg4 = float(self.r4rcc/1000)
        self.sC4 = True
        self.relay_Mcontroller4 = Clock.schedule_interval(self.relay_controller4,self.cg4)

    def r4Pause(self, instance):
        #GPIO.output(Relay4, GPIO.LOW)
        if(self.sC4 == False):
            print("Nope")
        else:
            if self.relay_Mcontroller4:
                self.relay_Mcontroller4.cancel()
                self.relay_Mcontroller4 = None

                self.r4pause.text = "Resume"   
                print("PAUSED")         
            else:
                self.relay_Mcontroller4 = Clock.schedule_interval(self.relay_controller4,self.cg4)
                self.r4pause.text = "Pause"
                print("RESUME")

    def r4Reset(self,instance):
        if(self.cycleCap4 == 0):
            print("NO RESET")
        else:
            self.cycles4 = 0
            print("RESETED")
            self.r4c.text = ("Current Cycles: " + str(self.cycles4))

    def relay_controller4(self,dt):
        if(self.r4rcM == 0):
            self.r4rc1 += 0.01
            if(self.r4rc1 <= self.etg4):
                print("Current Extend")
                #GPIO.output(Relay4, GPIO.HIGH)
            else:
                print("switching")
                self.r4rcM += 1
                self.r4rc1 = 0.0
        elif(self.r4rcM == 1):
            self.r4rc2 += 0.01
            if(self.r4rc2 <= self.rtg4):
                print("Current Retract")
                #GPIO.output(Relay4, GPIO.LOW)
            else:
                print("switching")
                self.r4rcM += 1
                self.r4rc2 = 0.0 
        elif(self.r4rcM == 2):
            self.cycles4 += 1    
            if(self.cycles4 >= self.cycleCap4):
                print("Stopped")
                print(self.cycleCap4)
                self.relay_Mcontroller4.cancel()
                #GPIO.output(Relay4, GPIO.LOW)

            else:
                self.r4c.text = "Current Cycles: " + str(self.cycles4)         
                self.r4rcM -= 2
                print("Completed 1 Cycle")
#######################################
    def Main_Menu_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'menu'

    def Relay_Settings_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'Relay_Settings' 

class Relay_Settings(Screen):
    relay_current = 0
    r1p = 1
    r2p = 1
    r3p = 1
    r4p = 1

    r1r = 500
    r2r = 500
    r3r = 500
    r4r = 500

    r1e = 500
    r2e = 500
    r3e = 500
    r4e = 500
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.path.isfile("relay_data.txt"):#Saves previous input to a txt file and redisplays it on launch
            with open("relay_data.txt", "r") as f:
                d = f.read().split(",")
                prev_preset = d[0]
                prev_timeE = d[1]
                prev_timeR = d[2]
        else:
            prev_preset = ""
            prev_timeE = ""
            prev_timeR = ""

        self.part2 =  GridLayout(cols=3, row_force_default=True, row_default_height=90,rows = 8,spacing = [1,1])
        self.part3 =  GridLayout(cols=4, row_force_default=True, row_default_height=50,rows = 1,spacing = [1,1])
        self.logo = Image(source=('logo.png'))
        self.part2.add_widget(self.logo)
        self.part2.add_widget(Label(text = "Relay Settings"))
        self.part2.add_widget(Label(text = "The Retract and Extend Fields\nare in Milliseconds"))

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


        self.part2.add_widget(self.part3)
        self.current_relay = Label(text = "Current Relay:")
        self.part2.add_widget(self.current_relay)

        self.part2.add_widget(Label(text = ""))


        self.preset = Label(text="Preset: ",font_size = 18)
        self.part2.add_widget(self.preset)
        
        self.presetI = CustomTextInput(multiline=False,font_size = 18,text = prev_preset)
        self.part2.add_widget(self.presetI)
        
        self.part2.add_widget(Label(text = ""))

        self.retract_time = Label(text = "Retract Time: ")
        self.part2.add_widget(self.retract_time)

        self.retract_timeI = CustomTextInput(multiline = False,font_size = 18, text = prev_timeR)
        self.part2.add_widget(self.retract_timeI)

        self.part2.add_widget(Label(text = ""))

        self.extend_time = Label(text = "Extend Time: ")
        self.part2.add_widget(self.extend_time)

        self.extend_timeI = CustomTextInput(multiline = False,font_size = 18,text = prev_timeE)
        self.part2.add_widget(self.extend_timeI)

        self.submitB = Button(text = "SUBMIT",font_size = 18)
        self.submitB.bind(on_press =self.Submit)
        self.part2.add_widget(self.submitB)
    
        self.MainMenu = Button(text = "Main Menu",font_size = 15)
        self.MainMenu.bind(on_press=self.Main_Menu_Button)
        self.part2.add_widget(self.MainMenu)

        self.Relay_RunnerB = Button(text = "Relay Runner",font_size = 15) 
        self.Relay_RunnerB.bind(on_press=self.Relay_Runner_button)
        self.part2.add_widget(self.Relay_RunnerB)

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
        print(self.relay_current)
        if(self.relay_current == 1):
            self.r1p = int(self.presetI.text)
            self.r1r = int(self.retract_timeI.text)
            self.r1e = int(self.extend_timeI.text)
            
            with open("relay_data.txt", "w") as f:#Writing previous input to local txt file
                f.write(f"{self.r1p},{self.r1r},{self.r1e},{self.r2p},{self.r2r},{self.r2e},{self.r3p},{self.r3r},{self.r3e},{self.r4p},{self.r4r},{self.r4e}")
            print(self.r1p,self.r1r,self.r1e)
        
        elif(self.relay_current == 2):
            self.r2p = int(self.presetI.text)
            self.r2r = int(self.retract_timeI.text)
            self.r2e = int(self.extend_timeI.text)
            
            with open("relay_data.txt", "w") as f:#Writing previous input to local txt file
                f.write(f"{self.r1p},{self.r1r},{self.r1e},{self.r2p},{self.r2r},{self.r2e},{self.r3p},{self.r3r},{self.r3e},{self.r4p},{self.r4r},{self.r4e}")
            print(self.r2p,self.r2r,self.r2e)     

        elif(self.relay_current == 3):
            self.r3p = int(self.presetI.text)
            self.r3r = int(self.retract_timeI.text)
            self.r3e = int(self.extend_timeI.text)
            
            with open("relay_data.txt", "w") as f:#Writing previous input to local txt file
                f.write(f"{self.r1p},{self.r1r},{self.r1e},{self.r2p},{self.r2r},{self.r2e},{self.r3p},{self.r3r},{self.r3e},{self.r4p},{self.r4r},{self.r4e}")
            print(self.r3p,self.r3r,self.r3e)  

        elif(self.relay_current == 4):
            self.r4p = int(self.presetI.text)
            self.r4r = int(self.retract_timeI.text)
            self.r4e = int(self.extend_timeI.text)
            with open("relay_data.txt", "w") as f:#Writing previous input to local txt file
                f.write(f"{self.r1p},{self.r1r},{self.r1e},{self.r2p},{self.r2r},{self.r2e},{self.r3p},{self.r3r},{self.r3e},{self.r4p},{self.r4r},{self.r4e}")
            print(self.r4p,self.r4r,self.r4e)        
    def Main_Menu_Button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'menu'
    def Relay_Runner_button(self, instance):
        app = App.get_running_app()
        app.sm.current = 'Relay_Runner' 

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
