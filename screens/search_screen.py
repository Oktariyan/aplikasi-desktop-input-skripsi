from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
import pandas as pd
import os
import sys
import subprocess

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

# Warna UI
BUTTON_COLOR = (0.184, 0.322, 0.627, 1)  # Warna navbar (#2f52a0)
TEXT_COLOR = (0, 0, 0, 1)  # Warna teks (hitam)
BACKGROUND_COLOR = (1, 1, 1, 1)  # Warna latar belakang (putih)
BORDER_COLOR = (0, 0, 0, 1)  # Warna border (hitam)

# Ukuran Window
Window.size = (800, 600)

class Navbar(BoxLayout):
    def __init__(self, back_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        self.padding = [20, 10]
        self.spacing = 15

        with self.canvas.before:
            Color(*BUTTON_COLOR)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        back_btn = Button(size_hint=(None, None), size=(65, 65), pos_hint={'center_y': 0.5},
                          background_normal='assets/icons/back_icon.png', background_down='assets/icons/back_icon.png')
        if back_callback:
            back_btn.bind(on_release=back_callback)
        self.add_widget(back_btn)

        logo = Image(source='assets/logo_unair.png', size_hint=(None, None), size=(50, 50))
        self.add_widget(logo)

        title_label = Label(text="RUANG BACA FAKULTAS SAINS DAN TEKNOLOGI", 
                          font_size=20, color=TEXT_COLOR, halign="left", valign="middle")
        title_label.bind(size=title_label.setter('text_size'))
        self.add_widget(title_label)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Tambahkan Navbar di atas
        navbar = Navbar(back_callback=self.go_back)
        layout.add_widget(navbar)

        # Area Konten
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        content.canvas.before.add(Color(*BACKGROUND_COLOR))
        content.canvas.before.add(Rectangle(pos=content.pos, size=content.size))
        content.bind(pos=self.update_rect, size=self.update_rect)

        # Pesan kesalahan
        self.message_label = Label(text="", font_size=16, color=(1, 0, 0, 1))
        content.add_widget(self.message_label)

        # Spinner untuk memilih sheet
        self.sheet_spinner = Spinner(text="Pilih Sheet", size_hint_y=None, height=40, 
                                   background_color=BUTTON_COLOR, color=(1, 1, 1, 1))
        self.sheet_spinner.bind(text=self.on_sheet_select)
        content.add_widget(self.sheet_spinner)

        # ScrollView untuk menampilkan data
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.data_grid = GridLayout(cols=1, size_hint_y=None)
        self.data_grid.bind(minimum_height=self.data_grid.setter('height'))
        self.scroll_view.add_widget(self.data_grid)
        content.add_widget(self.scroll_view)

        # Input untuk pencarian
        self.search_input = TextInput(hint_text="Cari data...", size_hint_y=None, height=40, 
                                    background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        content.add_widget(self.search_input)

        # Tombol untuk mencari data
        search_button = Button(text="Cari", size_hint_y=None, height=40, 
                              background_color=BUTTON_COLOR, color=(1, 1, 1, 1))
        search_button.bind(on_release=self.search_data)
        content.add_widget(search_button)

        # Tombol untuk membuka file Excel
        open_excel_button = Button(text="Buka File Excel", size_hint_y=None, height=40, 
                                  background_color=BUTTON_COLOR, color=(1, 1, 1, 1))
        open_excel_button.bind(on_release=self.open_excel_file)
        content.add_widget(open_excel_button)

        layout.add_widget(content)
        self.add_widget(layout)

        # Cek dan baca data
        self.check_and_display_data()

    def go_back(self, instance):
        self.manager.current = 'home'

    def check_and_display_data(self):
        file_path = "data_mahasiswa.xlsx"
        if os.path.exists(file_path):
            self.load_sheets(file_path)
        else:
            self.message_label.text = "File tidak ditemukan! Tolong buat atau isi input dulu."
            self.sheet_spinner.values = []

    def load_sheets(self, file_path):
        try:
            xl = pd.ExcelFile(file_path)
            self.sheet_spinner.values = xl.sheet_names
            self.sheet_spinner.text = xl.sheet_names[0] if xl.sheet_names else "Pilih Sheet"
            self.on_sheet_select(self.sheet_spinner, self.sheet_spinner.text)
        except Exception as e:
            self.message_label.text = f"Gagal memuat sheet: {str(e)}"
            self.sheet_spinner.values = []

    def on_sheet_select(self, spinner, text):
        file_path = "data_mahasiswa.xlsx"
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path, sheet_name=text)
                self.display_data(df)
            except Exception as e:
                self.message_label.text = f"Gagal memuat data: {str(e)}"
                self.data_grid.clear_widgets()
        else:
            self.message_label.text = "File tidak ditemukan! Tolong buat atau isi input dulu."

    def search_data(self, instance):
        file_path = "data_mahasiswa.xlsx"
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, sheet_name=self.sheet_spinner.text)
            search_term = self.search_input.text
            if search_term:
                result = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
                if not result.empty:
                    self.display_data(result)
                else:
                    self.message_label.text = "Data tidak ditemukan."
                    self.data_grid.clear_widgets()
            else:
                self.message_label.text = "Masukkan kata kunci pencarian."
                self.data_grid.clear_widgets()
        else:
            self.message_label.text = "File tidak ditemukan! Tolong buat atau isi input dulu."

    def display_data(self, df):
        self.data_grid.clear_widgets()
        self.data_grid.cols = len(df.columns)
        self.data_grid.size_hint_y = None
        self.data_grid.height = len(df) * 40

        # Tambahkan header
        for col in df.columns:
            header = Label(text=str(col), font_size=14, color=TEXT_COLOR, 
                          size_hint_y=None, height=40)
            with header.canvas.before:
                Color(*BORDER_COLOR)
                Line(rectangle=(header.x, header.y, header.width, header.height), width=1)
            self.data_grid.add_widget(header)

        # Tambahkan data
        for _, row in df.iterrows():
            for item in row:
                data_label = Label(text=str(item), font_size=12, color=TEXT_COLOR, 
                                 size_hint_y=None, height=40)
                with data_label.canvas.before:
                    Color(*BORDER_COLOR)
                    Line(rectangle=(data_label.x, data_label.y, data_label.width, data_label.height), width=1)
                self.data_grid.add_widget(data_label)

    def open_excel_file(self, instance):
        file_path = "data_mahasiswa.xlsx"
        if os.path.exists(file_path):
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS dan Linux
                subprocess.run(['open', file_path] if os.uname().sysname == 'Darwin' else ['xdg-open', file_path])
        else:
            self.message_label.text = "File tidak ditemukan! Tolong buat atau isi input dulu."

    def update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*BACKGROUND_COLOR)
            Rectangle(pos=instance.pos, size=instance.size)