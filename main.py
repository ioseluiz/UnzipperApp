from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from time import sleep
import threading
import os
import utils


# Designate our .kv design file
root_folder = os.getcwd()


global current
current = 0

class CustomDropDown(Button):
    def __init__(self, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.text = "Select Drive:"
        self.color = 1,0,1,1
        self.drop_list = None
        self.drop_list = DropDown()

        drives = utils.get_drives()
        for drive in drives:
            btn = Button(text=f"{drive}", size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))

            self.drop_list.add_widget(btn)

        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=lambda btn, x: setattr(self, 'text', x))


class InterfaceWindow(Screen):

    def unzip_files(self):
        print("Button Pressed!")
        thread_button = threading.Thread(target=self.update_progress)
        thread_button.start()
        Clock.schedule_interval(self.get_fromthread, 1)

    def update_file_drive(self):
        print("Cambio de Path en filechooser")
        ref_file_screen = self.manager.get_screen("filewindow")
        print(ref_file_screen)
        try:
            ref_file_screen.ids.filechooser.path = self.ids.dropdown.text
        except:
            print("Hay error en cambio de path")

    def update_folder_drive(self):
        print("Cambio de Path en filechooser")
        ref_file_screen = self.manager.get_screen("filewindow")
        print(ref_file_screen)
        try:
            ref_file_screen.ids.filechooser.path = self.ids.dropdown_folder.text
        except:
            print("Hay error en cambio de path")


class FileWindow(Screen):
  
    def selected(self, filename):
        print(filename)
        ref_interface_screen = self.manager.get_screen("main_window")
        print(ref_interface_screen)
        try:
           
            ref_interface_screen.ids.file_path.text = f"File Path: {filename[0]}"
        except:
            pass

    # def get_main_button_text(self):
    #     ref_interface_screen = self.manager.get_screen("main_window")
    #     print(ref_interface_screen)
    #     return ref_interface_screen.ids.dropdown.text

class FolderWindow(Screen):
    def selected(self, filename):
        print(filename)
        ref_interface_screen = self.manager.get_screen("main_window")
        print(ref_interface_screen)
        try:
           
            ref_interface_screen.ids.folder_path.text = f"Folder Path: {filename[0]}"
        except:
            pass


class UnzipperApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
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