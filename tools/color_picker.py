from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.clock import Clock
from device import device
from kivy.properties import ObjectProperty
KV = '''
<CustomImageColorPicker>:
    orientation: 'vertical'
    ImageColorPicker:
        source: '../img/klik.png'
'''

class CustomImageColorPicker(Widget):
    pass

class ImageColorPicker(Image):
    picker_item = ObjectProperty(None, allownone = True)
    def __init__(self, **kwargs):
        super(ImageColorPicker, self).__init__(**kwargs)
        self.active_touch = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active_touch = touch
            self.print_rgb()

    def on_touch_up(self, touch):
        self.active_touch = None

    def on_touch_move(self, touch):
        if self.active_touch and self.active_touch.uid == touch.uid:
            pass  # Nic nie rób podczas przesuwania dotyku

    def print_rgb(self):
        if self.active_touch:
            pos = self.active_touch.pos
            relative_pos = self.to_widget(*pos, relative=True)
            rgb = self.get_pixel_color(relative_pos)
            device.led.set_colour(*rgb)
            print(rgb)
            self.picker_item = rgb

    def get_pixel_color(self, pos):
        norm_x = pos[0] / self.width
        norm_y = pos[1] / self.height
        pixel_color = self.texture.get_region(int(norm_x * self.texture.width), int(norm_y * self.texture.height), 1, 1).pixels
        r, g, b = (
            int(pixel_color[0]),
            int(pixel_color[1]),
            int(pixel_color[2])
        )
        return r, g, b

class ColorPickerApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

