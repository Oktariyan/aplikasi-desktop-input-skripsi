from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
import os
import sys

# Enhanced resource path function
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    path = os.path.join(base_path, *relative_path.split('/'))
    path = os.path.normpath(path)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Resource not found: {path}")
    
    return path

# Window settings
Window.size = (800, 600)
Window.clearcolor = (1, 1, 1, 1)  # White background

# Color constants
BUTTON_COLOR = (0.18, 0.32, 0.63, 1)  # #2f52a0
MARQUEE_BG_COLOR = (1, 0.77, 0.04, 1)  # #ffc50b

class HoverButton(ButtonBehavior, BoxLayout):
    def __init__(self, text='', icon_path='', **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        self.size_hint = (0.3, 1)
        self.padding = [10, 20, 10, 10]
        self.spacing = 8
        self.orientation = 'vertical'
        self.default_color = BUTTON_COLOR
        self.hover_color = (0.22, 0.38, 0.75, 1)
        self.click_color = (0.15, 0.26, 0.52, 1)

        with self.canvas.before:
            self.shadow_color = Color(0, 0, 0, 0)
            self.shadow = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
            self.button_color = Color(*self.default_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

        if icon_path:
            try:
                self.icon = Image(
                    source=resource_path(icon_path), 
                    size_hint=(None, None), 
                    size=(65, 65), 
                    pos_hint={'center_x': 0.5, 'y': 2}
                )
                self.add_widget(self.icon)
            except Exception as e:
                print(f"Error loading icon: {e}")

        self.label = Label(
            text=text,
            font_size=25,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=30
        )
        self.add_widget(self.label)

        self.bind(pos=self.update_rect, size=self.update_rect)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.pos[0] - 5, self.pos[1] - 5)
        self.shadow.size = (self.size[0] + 10, self.size[1] + 10)

    def on_mouse_pos(self, window, pos):
        if self.collide_point(*pos):
            self.show_hover()
        else:
            self.hide_hover()

    def show_hover(self):
        Animation(a=0.4, duration=0.15).start(self.shadow_color)
        Animation(rgba=self.hover_color, duration=0.15).start(self.button_color)

    def hide_hover(self):
        Animation(a=0, duration=0.15).start(self.shadow_color)
        Animation(rgba=self.default_color, duration=0.15).start(self.button_color)

    def on_press(self):
        Animation(rgba=self.click_color, duration=0.1).start(self.button_color)

    def on_release(self):
        Animation(rgba=self.hover_color, duration=0.1).start(self.button_color)

class MarqueeLabel(BoxLayout):
    def __init__(self, text, **kwargs):
        super(MarqueeLabel, self).__init__(**kwargs)
        self.size_hint = (1, 0.08)
        self.padding = [10, 5, 10, 5]
        self.spacing = 10

        with self.canvas.before:
            Color(*MARQUEE_BG_COLOR)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.label = Label(
            text=text,
            font_size=30,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            text_size=(None, self.height),
            size_hint=(None, 1)
        )
        self.add_widget(self.label)
        self.animate_text()

    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def animate_text(self):
        self.label.texture_update()
        text_width = self.label.texture_size[0]
        self.label.width = text_width
        self.label.x = self.width

        animation = Animation(x=-text_width, duration=12, t='linear')
        animation.bind(on_complete=lambda *args: self.animate_text())
        animation.start(self.label)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Background with error handling
        try:
            bg_source = resource_path('assets/Background.jpeg')
            with self.canvas.before:
                self.bg_image = Rectangle(source=bg_source, size=Window.size, pos=self.pos)
        except Exception as e:
            print(f"Error loading background: {e}")
            with self.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                self.bg_image = Rectangle(size=Window.size, pos=self.pos)

        self.bind(size=self.update_bg, pos=self.update_bg)

        main_layout = BoxLayout(orientation='vertical')

        # Navbar
        navbar = BoxLayout(orientation='horizontal', size_hint=(1, 0.11), padding=10, spacing=10)
        with navbar.canvas.before:
            Color(*BUTTON_COLOR)
            self.rect_navbar = Rectangle(size=navbar.size, pos=navbar.pos)
        navbar.bind(size=self.update_navbar, pos=self.update_navbar)

        # Navbar components
        try:
            back_button = Button(
                background_normal=resource_path('assets/icons/back_icon.png'),
                background_down=resource_path('assets/icons/back_icon.png'),
                size_hint=(None, None),
                size=(65, 65),
                pos_hint={'center_y': 0.5},
                on_release=self.go_back
            )
            navbar.add_widget(back_button)
        except Exception as e:
            print(f"Error loading back button: {e}")

        try:
            logo = Image(
                source=resource_path("assets/logo_unair.png"), 
                size_hint=(None, None), 
                size=(70, 70), 
                pos_hint={'center_y': 0.5}
            )
            navbar.add_widget(logo)
        except Exception as e:
            print(f"Error loading logo: {e}")

        title = Label(
            text="[b]RUANG BACA FAKULTAS SAINS DAN TEKNOLOGI[/b]",
            markup=True,
            font_size=36,
            halign="left",
            valign="middle"
        )
        navbar.add_widget(title)

        # Marquee
        marquee = MarqueeLabel("SELAMAT DATANG DI SISTEM MANAGEMENT RUANG BACA FAKULTAS SAINS DAN TEKNOLOGI UNIVERSITAS AIRLANGGA")

        # Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=20, spacing=20)
        
        try:
            btn_input = HoverButton(
                text="INPUT DATA MAHASISWA", 
                icon_path=resource_path('assets/icons/input_icon.png')
            )
            btn_input.bind(on_release=self.go_to_input)
            button_layout.add_widget(btn_input)
        except Exception as e:
            print(f"Error creating input button: {e}")

        try:
            btn_search = HoverButton(
                text="CARI DATA", 
                icon_path=resource_path('assets/icons/search_icon.png')
            )
            btn_search.bind(on_release=self.go_to_search)
            button_layout.add_widget(btn_search)
        except Exception as e:
            print(f"Error creating search button: {e}")

        try:
            btn_exit = HoverButton(
                text="KELUAR", 
                icon_path=resource_path('assets/icons/exit_icon.png')
            )
            btn_exit.bind(on_release=self.exit_app)
            button_layout.add_widget(btn_exit)
        except Exception as e:
            print(f"Error creating exit button: {e}")

        # Assemble layout
        main_layout.add_widget(navbar)
        main_layout.add_widget(marquee)
        main_layout.add_widget(Widget(size_hint=(1, 0.55)))
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)

    def update_navbar(self, instance, value):
        self.rect_navbar.pos = instance.pos
        self.rect_navbar.size = instance.size

    def update_bg(self, *args):
        self.bg_image.size = Window.size
        self.bg_image.pos = self.pos

    def go_back(self, instance):
        App.get_running_app().stop()

    def exit_app(self, instance):
        App.get_running_app().stop()

    def go_to_input(self, instance):
        self.manager.current = 'input'

    def go_to_search(self, instance):
        self.manager.current = 'search'