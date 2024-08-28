from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from time import sleep
from unzip import get_file_info, extract_file
import threading
import os
import utils
from kivy.core.window import Window
import os



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
        
        self.schedule = Clock.schedule_interval(self.get_fromthread, 1)

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


    def update_progress(self):
        # Reset progress bar
        self.ids.my_progress_bar.value = 0
        
        # Read location of files and folder data
        file_for_unzip = self.ids.file_path.text
        file_for_unzip = file_for_unzip.replace("File Path: ","")
        destination_folder = self.ids.folder_path.text
        destination_folder = destination_folder.replace("Folder Path: ","")
        print(file_for_unzip)
        print(destination_folder)

        # Get list of files inside the zip file
        if file_for_unzip[-4:] == ".zip":
            list_of_files = get_file_info(file_for_unzip)
            print(list_of_files)

        print("thread_button started...")
        global current
        qty_files = len(list_of_files)
        list_test = [x for x in range(0,qty_files)]
        for file in list_of_files:
            # Grab the current progress bar value
            current = self.ids.my_progress_bar.value
            # Unzip file and copy in the destination folder
            extract_file(file_for_unzip, destination_folder, file)
            # Increment value
            current += 1/qty_files
            # print(current)
            # Update the progress bar
            sleep(1)
        print("thread_button_completed...")
        self.schedule.cancel()
        current = 0

        return
            
    def get_fromthread(self, *args):
        print(current)
        self.ids.my_label.text = f"{round(current * 100,0)} % Progress"
        self.ids.my_progress_bar.value = current


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
       
    
        
if __name__ == "__main__":
    # Kivy Window Size
    Window.size = (700, 770)
    thread_main = threading.Thread(target=UnzipperApp().run())