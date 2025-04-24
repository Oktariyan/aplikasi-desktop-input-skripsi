import os
import sys
from create_icon import create_ico

# Fungsi untuk mendapatkan path resources yang kompatibel dengan PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    path = os.path.join(base_path, *relative_path.split('/'))
    return os.path.normpath(path)

# Cek dan buat icon jika belum ada
if not os.path.exists(resource_path('assets/logo_unair.ico')):
    try:
        create_ico()
    except Exception as e:
        print(f"Error creating icon: {e}")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.search_screen import SearchScreen
from screens.input_screen import InputScreen

class RuangBacaApp(App):
    def build(self):
        # Menghapus registrasi font khusus dan menggunakan font default Kivy
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))  
        sm.add_widget(SearchScreen(name='search'))  
        sm.add_widget(InputScreen(name='input'))  
        return sm

if __name__ == '__main__':
    RuangBacaApp().run()