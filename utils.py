import win32api

def get_drives():
    drives = win32api.GetLogicalDriveStrings()
    drives_splitted = drives.split('\000')[:-1]
    print(drives_splitted)
    return drives_splitted
