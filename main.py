from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.search_screen import SearchScreen
from screens.input_screen import InputScreen

class ArsipApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))  
        sm.add_widget(SearchScreen(name='search'))  
        sm.add_widget(InputScreen(name='input'))  
        return sm

if __name__ == '__main__':
    ArsipApp().run()
