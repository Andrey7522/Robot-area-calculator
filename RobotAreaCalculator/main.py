from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Class for Robot draw-----------------------
class RobotCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.area = 0
        self.robotsize = 0
        self.objects = 0
        self.rad = 0
        self.mimum = 0
        self.midle = 0
        self.maximum = 0
        self.cell = 0
        self.needs_redraw = True

    def update_data(self, area, robotsize, objects):
        self.area = area
        self.robotsize = robotsize
        self.objects = objects
        self.rad = area + robotsize + objects
        self.mimum = self.rad * 0.25
        self.midle = self.rad * 0.60
        self.maximum = self.rad * 0.90
        self.cell = self.rad + 500
        self.needs_redraw = True
        self.canvas.clear()
        self.draw()

    def on_size(self, *args):
        # When the widget is resized, I redraw it
        if hasattr(self, 'needs_redraw') and self.needs_redraw:
            self.canvas.clear()
            self.draw()

    def draw(self):
        if self.rad == 0:
            return

        w = self.width
        h = self.height
        cx = w / 2
        cy = h / 2 + 20

        max_r = max(self.cell, self.maximum)
        if max_r == 0:
            return
        scale = min(w, h) / (max_r * 2.2)

        with self.canvas:
            # Cell (contour)
            Color(0.4, 0.4, 0.4, 1)
            cell_size = self.cell * scale * 2
            Line(rectangle=(cx - cell_size / 2, cy - cell_size / 2, cell_size, cell_size), width=2)


            Color(1, 1, 1, 1)
            Label(text=f"Area: {self.cell:.0f} мм",
                  pos=(cx - cell_size / 2 + 10, cy + cell_size / 2 - 30),
                  font_size='14sp').canvas

            # Max area (red)
            Color(1, 0, 0, 1)
            r_max = self.maximum * scale
            Line(circle=(cx, cy, r_max), width=2)

            # Work area (yellow)
            Color(1, 1, 0, 1)
            r_mid = self.midle * scale
            Line(circle=(cx, cy, r_mid), width=2)

            # Min area (green)
            Color(0, 1, 0, 1)
            r_min = self.mimum * scale
            Line(circle=(cx, cy, r_min), width=2)

            # Robor (orange)
            Color(1, 0.6, 0, 1)
            r_robot = 12 * scale
            Ellipse(pos=(cx - r_robot, cy - r_robot), size=(r_robot * 2, r_robot * 2))

# Windows:
class MainWindow(Screen):
    def on_enter(self):
        # Откладываем установку картинки, чтобы виджет успел создаться
        Clock.schedule_once(self.set_image, 0.1)

    def set_image(self, dt):
        self.ids.main_image.source = resource_path('picture/pxArt.ico')

class SecondWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self.check_fields)

    def check_fields(self, *args):
        # Checking whether
        area = self.ids.area.text.strip()
        robotsize = self.ids.robotsize.text.strip()
        objects = self.ids.objects.text.strip()

        # If all fields are filled in, show the button
        if area and robotsize and objects:
            self.ids.next_button.disabled = False
            self.ids.next_button.opacity = 1
        else:
            self.ids.next_button.disabled = True
            self.ids.next_button.opacity = 0.3

class ThirdWindow(Screen):
    def on_enter(self):
        try:
            area = float(self.manager.get_screen('second').ids.area.text)
            robotsize = float(self.manager.get_screen('second').ids.robotsize.text)
            objects = float(self.manager.get_screen('second').ids.objects.text) if self.manager.get_screen(
                'second').ids.objects.text else 0
        except:
            area = 0
            robotsize = 0
            objects = 0

        self.ids.robot_canvas.update_data(area, robotsize, objects)
        self.update_table()

    def update_table(self):
        canvas = self.ids.robot_canvas
        self.ids.t_min.text = f"{canvas.mimum:.0f} мм"
        self.ids.t_mid.text = f"{canvas.midle:.0f} мм"
        self.ids.t_max.text = f"{canvas.maximum:.0f} мм"
        self.ids.t_cell.text = f"{canvas.cell:.0f} мм"
        self.ids.t_rad.text = f"{canvas.rad:.0f} мм"

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('Test.kv')

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyMainApp().run()

