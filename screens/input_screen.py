from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from tkinter import Tk, filedialog

# Registrasi font Roboto
LabelBase.register(name="Roboto", fn_regular="assets/fonts/roboto-regular.ttf")
LabelBase.register(name="Roboto2", fn_regular="assets/fonts/Roboto_Condensed-Bold.ttf")

# Atur ukuran window
Window.size = (800, 600)

# Warna tombol
BUTTON_COLOR = (0.184, 0.322, 0.627, 1)  # Warna navbar (#2f52a0)
BUTTON_HOVER_COLOR = (0.15, 0.26, 0.52, 1)  # Warna hover (#26428a)
RED_COLOR = (1, 0, 0, 1)  # Warna merah untuk peringatan

used_numbers = set()  # Menyimpan no urut yang telah digunakan

class Navbar(BoxLayout):
    def __init__(self, back_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        self.padding = [20, 10]  # Padding: [kiri/kanan, atas/bawah]
        self.spacing = 15  # Jarak antar widget di navbar

        with self.canvas.before:
            Color(*BUTTON_COLOR)  # Warna navbar
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        back_btn = Button(size_hint=(None, None), size=(65, 65), pos_hint={'center_y': 0.5},
                          background_normal='assets/icons/back_icon.png', background_down='assets/icons/back_icon.png')
        if back_callback:
            back_btn.bind(on_release=back_callback)
        self.add_widget(back_btn)

        logo = Image(source='assets/logo_unair.png', size_hint=(None, None), size=(50, 50), pos_hint={'center_y': 0.5})
        self.add_widget(logo)

        title_label = Label(text="ARSIP FAKULTAS SAINS DAN TEKNOLOGI", font_name="Roboto2", font_size=20,
                            color=(1, 1, 1, 1), halign="left", valign="middle")
        title_label.bind(size=title_label.setter('text_size'))
        self.add_widget(title_label)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)  # Latar putih
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.selected_file = ""  # Menyimpan file yang dipilih
        self.warning_label = Label(text="", font_name="Roboto", font_size=14, color=RED_COLOR, size_hint=(1, 0.05), halign="center")

        main_layout = BoxLayout(orientation="vertical", padding=[20, 10], spacing=10)  # Padding dan spacing di layout utama
        main_layout.add_widget(Navbar(back_callback=self.go_back))

        title_layout = BoxLayout(size_hint=(1, 0.12), padding=[0, 10])
        title = Label(text="INPUT ARSIP", font_size=24, font_name="Roboto", size_hint=(1, 1),
                      color=(0, 0, 0, 1), halign="center", valign="middle")
        title.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        title_layout.add_widget(title)
        main_layout.add_widget(title_layout)

        scroll = ScrollView(size_hint=(1, 0.7))  # Hapus padding dari ScrollView
        form_layout = GridLayout(cols=2, spacing=15, padding=[20, 10], size_hint_y=None, row_default_height=50)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        labels = ["No Urut", "No Boks", "No Berkas", "Kode Klasifikasi", "Indeks/Nama Berkas", "Urai Informasi Arsip", "Kurun Waktu"]
        self.inputs = {}

        for label_text in labels:
            form_layout.add_widget(Label(text=label_text, font_name="Roboto", color=(0, 0, 0, 1), halign="right", valign="middle"))
            input_field = TextInput(multiline=False, font_name="Roboto", halign="center", size_hint_y=None, height=40)
            form_layout.add_widget(input_field)
            self.inputs[label_text] = input_field

        form_layout.add_widget(Label(text="Jangka Simpan", font_name="Roboto", color=(0, 0, 0, 1), halign="right", valign="middle"))
        self.spinner_jangka = Spinner(text="Pilih", values=["Aktif", "Inaktif"], font_name="Roboto", size_hint_y=None, height=40)
        form_layout.add_widget(self.spinner_jangka)

        form_layout.add_widget(Label(text="Kategori Arsip", font_name="Roboto", color=(0, 0, 0, 1), halign="right", valign="middle"))
        self.spinner_kategori = Spinner(text="Pilih", values=["AV: Arsip Vital", "AT: Arsip Terjaga", "R: Rahasia", "T: Terjaga"], font_name="Roboto", size_hint_y=None, height=40)
        form_layout.add_widget(self.spinner_kategori)

        form_layout.add_widget(Label(text="Deskripsi (Opsional)", font_name="Roboto", color=(0, 0, 0, 1), halign="right", valign="middle"))
        self.deskripsi_input = TextInput(multiline=True, font_name="Roboto", halign="center", size_hint_y=None, height=100)
        form_layout.add_widget(self.deskripsi_input)

        form_layout.add_widget(Label(text="Upload Berkas", font_name="Roboto", color=(0, 0, 0, 1), halign="right", valign="middle"))
        upload_btn = Button(text="Pilih File", font_name="Roboto", background_color=BUTTON_COLOR, size_hint_y=None, height=40)
        upload_btn.bind(on_release=self.open_file_dialog)
        form_layout.add_widget(upload_btn)

        scroll.add_widget(form_layout)
        main_layout.add_widget(scroll)
        main_layout.add_widget(self.warning_label)

        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=20, padding=[20, 10])  # Padding dan spacing di tombol
        clear_btn = Button(text="CLEAR", background_color=BUTTON_COLOR, font_name="Roboto")
        submit_btn = Button(text="SUBMIT", background_color=BUTTON_COLOR, font_name="Roboto")
        clear_btn.bind(on_release=self.clear_form)
        submit_btn.bind(on_release=self.submit_form)
        button_layout.add_widget(clear_btn)
        button_layout.add_widget(submit_btn)

        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def open_file_dialog(self, instance):
        root = Tk()
        root.withdraw()  # Sembunyikan jendela utama Tkinter
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg"), ("PDF files", "*.pdf")])
        if file_path:
            self.selected_file = file_path
            self.warning_label.text = f"File dipilih: {file_path.split('/')[-1]}"
        else:
            self.warning_label.text = "Tidak ada file yang dipilih."
        root.destroy()

    def clear_form(self, instance):
        for input_field in self.inputs.values():
            input_field.text = ""
        self.spinner_jangka.text = "Pilih"
        self.spinner_kategori.text = "Pilih"
        self.deskripsi_input.text = ""
        self.selected_file = ""
        self.warning_label.text = "Form dibersihkan."

    def submit_form(self, instance):
        missing_fields = [label for label, input_field in self.inputs.items() if not input_field.text.strip()]
        no_urut = self.inputs["No Urut"].text.strip()

        if no_urut in used_numbers:
            self.warning_label.text = "No Urut sudah digunakan."
            return

        if self.spinner_jangka.text == "Pilih":
            missing_fields.append("Jangka Simpan")
        if self.spinner_kategori.text == "Pilih":
            missing_fields.append("Kategori Arsip")

        if missing_fields:
            self.warning_label.text = "Form belum lengkap."
        else:
            used_numbers.add(no_urut)
            self.warning_label.text = "Form berhasil disubmit."
            print(f"Data tersimpan dengan file: {self.selected_file if self.selected_file else 'Tidak ada file'}")

    def go_back(self, instance):
        self.manager.current = 'home'  # Kembali ke HomeScreen

if __name__ == '__main__':
    sm = ScreenManager()
    sm.add_widget(InputScreen(name="input"))

    class ArsipApp(App):
        def build(self):
            return sm

    ArsipApp().run()