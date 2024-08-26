from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from time import sleep
import threading
import os


# Designate our .kv design file
root_folder = os.getcwd()


global current
current = 0

class InterfaceWindow(Screen):
    def unzip_files(self):
        print("Button Pressed!")
        thread_button = threading.Thread(target=self.update_progress)
        thread_button.start()
        Clock.schedule_interval(self.get_fromthread, 1)

class FileWindow(Screen):
    def selected(self, filename):
        print(filename)
        ref_interface_screen = self.manager.get_screen("main_window")
        print(ref_interface_screen)
        try:
           
            ref_interface_screen.ids.file_path.text = f"File Path: {filename[0]}"
        except:
            pass
class FolderWindow(Screen):
    pass


class UnzipperApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root = Builder.load_file('design.kv')
        sm = ScreenManager()
        sm.add_widget(InterfaceWindow(name='main_window'))
        sm.add_widget(FileWindow(name='filewindow'))
        sm.add_widget(FolderWindow(name='folderwindow'))
        return sm
       
    def update_progress(self):
        print("thread_button started...")
        global current
        for i in range(1,11):
            # Grab the current progress bar value
            current = self.ids.my_progress_bar.value
            # Increment value
            current += i/10
            # print(current)
            # Update the progress bar
            sleep(1)
        print("thread_button_completed...")
            
    def get_fromthread(self, *args):
        print(current)
        self.ids.my_label.text = f"{round(current,2)}"
        self.ids.my_progress_bar.value = current
        
if __name__ == "__main__":
    thread_main = threading.Thread(target=UnzipperApp().run())