from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from utils.database import lihat_arsip

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.bind(size=self.update_background)

        # Warna background utama putih
        with self.canvas.before:
            Color(1, 1, 1, 1)  
            self.rect = Rectangle(size=self.size, pos=self.pos)

        arsip_data = lihat_arsip()

        if arsip_data:
            scroll = ScrollView(size_hint=(1, 1))  # Ukuran proporsional agar tidak turun ke bawah

            grid = GridLayout(cols=9, size_hint_y=None, spacing=2)
            grid.bind(minimum_height=grid.setter('height'))

            # Container untuk header agar warna background bisa berubah
            header_container = GridLayout(cols=9, size_hint_y=None, height=40)
            header_container.bind(size=self.update_header_background)

            # Header tabel dengan latar belakang abu-abu
            headers = [
                "No Urut", "No Berkas", "Kode Klasifikasi", "Indeks/Nama Berkas",
                "Urai Informasi Arsip", "Kurun Waktu", "Jangka Simpan", "Kategori Arsip", "Deskripsi"
            ]
            for header in headers:
                header_label = Label(text=header, bold=True, size_hint_y=None, height=40, color=(1, 1, 1, 1))
                header_container.add_widget(header_label)

            # Tambahkan latar belakang untuk header
            with header_container.canvas.before:
                Color(0.2, 0.2, 0.2, 1)  # Warna abu-abu gelap
                self.header_bg = Rectangle(size=header_container.size, pos=header_container.pos)

            # Isi tabel
            for item in arsip_data:
                for i in range(1, 10):  # Ambil 9 kolom pertama (sesuai header)
                    grid.add_widget(Label(text=str(item[i]), size_hint_y=None, height=30, color=(0, 0, 0, 1)))

            scroll.add_widget(grid)
            self.add_widget(header_container)  # Header tetap di atas
            self.add_widget(scroll)
        else:
            self.add_widget(Label(text="Tidak ada data arsip", font_size=20, color=(0, 0, 0, 1)))

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_header_background(self, instance, value):
        """Memperbarui latar belakang header agar tetap sesuai ukuran"""
        self.header_bg.size = instance.size
        self.header_bg.pos = instance.pos

class ArsipApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    ArsipApp().run()
