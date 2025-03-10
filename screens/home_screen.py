from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.text import LabelBase
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior

# Daftarkan font Roboto
LabelBase.register(name="Roboto", fn_regular="assets/fonts/Roboto-Regular.ttf")
LabelBase.register(name="Roboto2", fn_regular="assets/fonts/Roboto_Condensed-Bold.ttf")

# Atur ukuran dan warna jendela
Window.size = (800, 600)
Window.clearcolor = (1, 1, 1, 1)  # Background default (akan ditutupi gambar)

BUTTON_COLOR = (0.18, 0.32, 0.63, 1)  # Warna #2f52a0
MARQUEE_BG_COLOR = (1, 0.77, 0.04, 1)  # Warna #ffc50b

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
            self.icon = Image(source=icon_path, size_hint=(None, None), size=(65, 65), pos_hint={'center_x': 0.5, 'y': 2})
            self.add_widget(self.icon)

        self.label = Label(
            text=text,
            font_name="Roboto2",
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
        if self.get_root_window() and self.collide_point(*pos):
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
            font_name="Roboto2",
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

        with self.canvas.before:
            self.bg_image = Rectangle(source='assets/Background.jpeg', size=Window.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        main_layout = BoxLayout(orientation='vertical')

        navbar = BoxLayout(orientation='horizontal', size_hint=(1, 0.11), padding=10, spacing=10)
        with navbar.canvas.before:
            Color(*BUTTON_COLOR)
            self.rect_navbar = Rectangle(size=navbar.size, pos=navbar.pos)
        navbar.bind(size=self.update_navbar, pos=self.update_navbar)

        back_button = Button(
            background_normal='assets/icons/back_icon.png',
            background_down='assets/icons/back_icon.png',
            size_hint=(None, None),
            size=(65, 65),
            pos_hint={'center_y': 0.5},
            on_release=self.go_back
        )

        logo = Image(source="assets/logo_unair.png", size_hint=(None, None), size=(70, 70), pos_hint={'center_y': 0.5})
        title = Label(
            text="[b]ARSIP FAKULTAS SAINS DAN TEKNOLOGI[/b]",
            markup=True,
            font_name="Roboto2",
            font_size=36,
            halign="left",
            valign="middle"
        )

        navbar.add_widget(back_button)
        navbar.add_widget(logo)
        navbar.add_widget(title)

        marquee = MarqueeLabel("SELAMAT DATANG DI SISTEM ARSIP FAKULTAS SAINS DAN TEKNOLOGI UNIVERSITAS AIRLANGGA")

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=20, spacing=20)
        btn_input = HoverButton(text="INPUT DATA ARSIP", icon_path='assets/icons/input_icon.png')
        btn_search = HoverButton(text="CARI ARSIP", icon_path='assets/icons/search_icon.png')
        btn_exit = HoverButton(text="KELUAR", icon_path='assets/icons/exit_icon.png')
        btn_exit.bind(on_release=self.exit_app)

        # Bind tombol input dan search ke fungsi pindah layar
        btn_input.bind(on_release=self.go_to_input)
        btn_search.bind(on_release=self.go_to_search)

        button_layout.add_widget(btn_input)
        button_layout.add_widget(btn_search)
        button_layout.add_widget(btn_exit)

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

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super(InputScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        label = Label(text="Halaman Input Data Arsip", font_size=30, font_name="Roboto2")
        btn_back = Button(text="Kembali ke Home", size_hint=(0.3, 0.1), on_release=self.go_back)

        layout.add_widget(label)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        label = Label(text="Halaman Cari Data Arsip", font_size=30, font_name="Roboto2")
        btn_back = Button(text="Kembali ke Home", size_hint=(0.3, 0.1), on_release=self.go_back)

        layout.add_widget(label)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class ArsipApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(InputScreen(name='input'))
        sm.add_widget(SearchScreen(name='search'))
        return sm

if __name__ == '__main__':
    ArsipApp().run()