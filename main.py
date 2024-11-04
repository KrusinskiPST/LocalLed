from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from device import device
from kivy.uix.image import Image
from kivy.clock import Clock
from tools.color_picker import ColorPickerApp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.graphics import BorderImage
import time
Builder.load_file('main.kv')

class GUI(Widget):
    def status_reader(self):
        data = device.led.status()
        isON = data['dps'].get('20')
        
        if isON:
            self.powerbutton_on()
        else:
            self.powerbutton_off()


    def powerbutton_detector(self):
        btn = self.ids.power_button
        if btn.source == 'img/Off.ico':
            self.powerbutton_on()
        else:
            self.powerbutton_off()
        print(device.led.status())

    def powerbutton_on(self):
        btn = self.ids.power_button
        btn.source = 'img/On.ico'
        btn.background_color = (0, 1, 0, 1)
        device.led.turn_on()

    def powerbutton_off(self):
        btn = self.ids.power_button
        btn.source = 'img/Off.ico'
        device.led.turn_off()

    def on_slider_value_change(self, *args):
        self.value = args[1]
        self.jasnosc = self.value / 10
        self.ids.label.text = "Janość: {:.0f}%".format(self.jasnosc)
        Clock.unschedule(self.update_device_led)
        Clock.schedule_once(self.update_device_led, 0.3)

    def update_device_led(self, dp):
        device.led.set_brightness(self.value)
        

    def options(self):
        new_box = self.ids.new_box  # Pobieramy nowy BoxLayout za pomocą ids
        scene = self.ids.scene
        if new_box.opacity == 0:  # Jeśli jest ukryty
            new_box.y = self.height  # Początkowa pozycja na samym dole
            anim = Animation(opacity=1, y=self.parent.height - new_box.height, duration=0.3)  # Animacja pojawienia się z góry
            anim.start(new_box)
            anim.bind(on_complete=lambda *args: setattr(new_box, 'disabled', False))
        else:
            anim = Animation(opacity=0, y=self.height, duration=0.2)  # Animacja zniknięcia w górę
            anim.start(new_box)
            anim.bind(on_complete=lambda *args: setattr(new_box, 'disabled', True))
            
        if scene.opacity == 0:
            anim = Animation(opacity=1, duration=0.2)
            anim.start(scene)
            anim.bind(on_complete=lambda *args: setattr(scene, 'disabled', False))
        else:
            anim = Animation(opacity=0, duration=0.2)
            anim.start(scene)
            anim.bind(on_complete=lambda *args: setattr(scene, 'disabled', True))


    #Scenario funcions   
    def nature(self):
        device.led.set_mode(mode = 'white')

    def night(self):
        device.led.set_colour(178, 228, 251)

    def read(self):
        device.led.set_mode(21, 'white')

    def rave(self):
        device.led.set_value(21, 'music', nowait = True)

    def rainbow(self):
        device.led.set_value(21, 'scene')
        device.led.set_value(25, '06646401000003e803e800000000646401007803e803e80000000064640100f003e803e800000000646401012e03e803e800000000646401003f03e803e800000000646401016803e803e800000000646401009003e803e80000000064640100c003e803e800000000',nowait = True)

class Led_control(App):
    def build(self):
        Window.clearcolor = hex('#0b2a3c')
        gui = GUI()
        gui.status_reader()
        
        Window.size = (770, 740)
        return gui

if __name__ == '__main__':
    Led_control().run()
