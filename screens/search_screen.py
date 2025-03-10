from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Daftarkan font Roboto
LabelBase.register(name='Roboto', fn_regular='assets/fonts/roboto-regular.ttf')
LabelBase.register(name='Roboto2', fn_regular='assets/fonts/Roboto_Condensed-Bold.ttf')

# Ukuran dan rasio layar
Window.size = (800, 600)
Window.minimum_width = 500
Window.minimum_height = 300

# Warna
NAVBAR_COLOR = (0.18, 0.32, 0.63, 1)  # Warna navbar (#2f52a0)
BUTTON_COLOR = (0.16, 0.43, 0.75, 1)  # Warna tombol (#2a6fbf)
BACKGROUND_COLOR = (1, 1, 1, 1)  # Latar belakang putih
ROW_COLOR = (0.95, 0.95, 0.95, 1)  # Warna baris tabel

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(*BACKGROUND_COLOR)  # Latar belakang putih
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Navbar
        navbar = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), padding=[20, 10], spacing=15)
        with navbar.canvas.before:
            Color(*NAVBAR_COLOR)  # Warna latar navbar
            self.navbar_rect = Rectangle(size=navbar.size, pos=navbar.pos)
        navbar.bind(size=self.update_navbar_rect, pos=self.update_navbar_rect)

        # Tombol Kembali
        back_button = Button(
            background_normal='assets/icons/back_icon.png',  # Pastikan path ini valid
            size_hint=(None, None),  # Ukuran tidak diatur relatif
            size=(50, 50),  # Ukuran tombol 50x50 piksel
            pos_hint={'center_y': 0.5},  # Posisi vertikal di tengah
            background_down='assets/icons/back_icon.png',  # Ikon saat tombol ditekan
            background_color=(1, 1, 1, 1)  # Latar belakang putih (untuk debugging)
        )
        back_button.bind(on_press=self.on_back_button_press)

        # Logo
        logo = Image(source='assets/logo_unair.png', size_hint=(None, None), size=(50, 50), pos_hint={'center_y': 0.5})

        # Judul Navbar
        title = Label(
            text="ARSIP FAKULTAS SAINS DAN TEKNOLOGI",
            font_name="Roboto2",
            font_size=20,
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
            size_hint=(1, 1))
        title.bind(size=title.setter('text_size'))

        # Tambahkan widget ke navbar
        navbar.add_widget(back_button)
        navbar.add_widget(logo)
        navbar.add_widget(title)

        # Tambahkan navbar ke layout utama
        main_layout.add_widget(navbar)

        # Judul Halaman
        title_label = Label(
            text="PENCARIAN ARSIP",
            font_name="Roboto",
            font_size=28,
            size_hint=(1, 0.1),
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1))
        title_label.bind(size=title_label.setter('text_size'))
        main_layout.add_widget(title_label)

        # Form Pencarian
        form_container = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=120, padding=[20, 10])

        form_layout = GridLayout(cols=4, spacing=10, size_hint=(1, 1))

        # Item Form
        form_items = [
            ("Jangka Simpan:", Spinner(text="Pilih Jangka Simpan", values=["Aktif", "Inaktif"], size_hint=(1, None), height=40)),
            ("Kategori Arsip:", Spinner(text="Pilih Kategori", values=["AV: Arsip Vital", "AT: Arsip Terjaga", "R: Rahasia", "T: Terjaga"], size_hint=(1, None), height=40)),
            ("No Urut:", TextInput(hint_text="Masukkan No Urut", size_hint=(1, None), height=40)),
            ("Kata Kunci:", TextInput(hint_text="Masukkan kata kunci", size_hint=(1, None), height=40))
        ]

        for label_text, widget in form_items:
            label = Label(
                text=label_text,
                font_name="Roboto",
                font_size=18,
                halign="right",
                valign="middle",
                color=(0, 0, 0, 1),
                size_hint=(0.5, None),
                height=40
            )
            label.bind(size=label.setter('text_size'))

            widget.font_name = "Roboto"
            widget.font_size = 16

            form_layout.add_widget(label)
            form_layout.add_widget(widget)

        form_container.add_widget(form_layout)
        main_layout.add_widget(form_container)

        # Tombol Cari
        search_button = Button(
            text="CARI",
            font_name="Roboto",
            font_size=18,
            size_hint=(1, None),
            height=50,
            background_color=BUTTON_COLOR
        )
        main_layout.add_widget(search_button)

        # Header Tabel
        table_header = GridLayout(cols=8, spacing=5, size_hint=(1, None), height=40, padding=[5, 0])
        headers = ["No", "No Urut", "No Boks", "No Berkas", "Kode Klasifikasi", "Nama Berkas", "Kurun Waktu", "Edit"]
        for header in headers:
            lbl = Label(text=header, font_name="Roboto", font_size=16, bold=True, color=(0, 0, 0, 1), halign="center", valign="middle")
            lbl.bind(size=lbl.setter('text_size'))
            table_header.add_widget(lbl)
        main_layout.add_widget(table_header)

        # ScrollView Hasil Pencarian
        scroll_view = ScrollView(size_hint=(1, 0.6))
        result_layout = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=[5, 0])
        result_layout.bind(minimum_height=result_layout.setter('height'))

        for i in range(1, 11):
            row = GridLayout(cols=8, size_hint_y=None, height=40, padding=[5, 0], spacing=5)
            with row.canvas.before:
                Color(*ROW_COLOR)
                Rectangle(size=row.size, pos=row.pos)
            row.bind(size=self.update_row_rect, pos=self.update_row_rect)

            row_data = [
                str(i), str(100 + i), f"Boks {i}", f"Berkas {i}", "001/ABC",
                f"Dokumen {i}", "2020-2022"
            ]

            for data in row_data:
                lbl = Label(text=data, font_name="Roboto", font_size=16, color=(0, 0, 0, 1), halign="center", valign="middle")
                lbl.bind(size=lbl.setter('text_size'))
                row.add_widget(lbl)

            edit_btn = Button(
                text="EDIT",
                font_name="Roboto",
                font_size=16,
                size_hint=(1, None),
                height=30,
                background_color=BUTTON_COLOR,
                color=(1, 1, 1, 1)
            )
            row.add_widget(edit_btn)
            result_layout.add_widget(row)

        scroll_view.add_widget(result_layout)
        main_layout.add_widget(scroll_view)

        self.add_widget(main_layout)

    def update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def update_navbar_rect(self, instance, value):
        self.navbar_rect.size = instance.size
        self.navbar_rect.pos = instance.pos

    def update_row_rect(self, instance, value):
        for instr in instance.canvas.before.children:
            if isinstance(instr, Rectangle):
                instr.size = instance.size
                instr.pos = instance.pos

    def on_back_button_press(self, instance):
        print("Tombol back ditekan!")
        # Tambahkan logika navigasi ke halaman sebelumnya di sini

class ArsipApp(App):
    def build(self):
        return SearchScreen()

if __name__ == '__main__':
    ArsipApp().run()