from pathlib import Path
from zipfile import ZipFile, ZipInfo

def get_file_info(filepath: str) -> list[ZipInfo]:
    with ZipFile(filepath, 'r') as zObject:
        list_files = zObject.infolist()
    return list_files

def extract_file(filepath:str, destination_folder: str, item: ZipInfo) -> None:
    new_path = Path(r"\\?\\" + destination_folder)
    with ZipFile(filepath, 'r') as zObject:
        list_files = zObject.infolist()
        print(f"item: {item}")
        print(type(item))
        print(list_files[0])
        print(type(list_files[0]))
        print(list_files)

        try:
            found_item = next(x for x in list_files if x.filename == item.filename)
        except StopIteration:
            raise IndexError("Couldn't find item")
        # found_item = [x for x in list_files if x == item]
        print(found_item)

        if found_item:
            zObject.extract(found_item.filename, path=new_path)
            print(f"{found_item.filename} extracted into {destination_folder}")
        # for info in list_files:
        #     zObject.extract(info.filename, path=new_path)