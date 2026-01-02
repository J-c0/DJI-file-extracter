import os
import shutil


update_existing = True

redirect_path = 'C:\your\new\path\DJI_001'
target_path = 'F:\DCIM\DJI_001'


def check_existing_folder(path):    
    global exist_folders
    global redirect_path

    check_path = os.walk(redirect_path)

    exist_folders = {}
    for root, dirs, files in check_path:
        
        path = str(root)
        if path == redirect_path:
            continue

        path = path[len(redirect_path)+1:len(redirect_path)+11]
        root = root[len(redirect_path)+1:]

        exist_folders.update({path : root})


check_existing_folder(redirect_path)


def create_dir(name):
    global redirect_path
    
    if name in exist_folders:
        print(f'Folder {name} already exists')
        return
    try:
        os.mkdir(f'{redirect_path}\{name}')
    except FileExistsError:
        print(f'Folder {name} already exists')
        
    else:
        print(f'Folder {name} created')

try:
    files = os.walk(target_path)
except Exception as e:
    print('Error accessing target path', e)
    exit()

    


for root, dirs, file_names in files:

    date_set = set({})
    for file in file_names:
        
        if 'DJI_' in file:
            
            date = file.split('_')
            date = date[1]
            date = date[:8]
            # date : yyyymmdd

            if date not in date_set:
                date_set.add(date)
                new_file_name = f'{date[:4]}_{date[4:6]}_{date[6:10]}'
                # yyyy_mm_dd
                create_dir(new_file_name)
            
            if new_file_name in exist_folders.keys():
                if update_existing:
                    new_file_name = exist_folders[new_file_name]
                else:
                    continue
            shutil.copyfile(f'{target_path}\\{file}',f'{redirect_path}\\{new_file_name}\\{file}')

        else:
            raise Exception('File unexpected', file)
        
if 'root' not in locals():
    raise Exception('No files found in target path')
print('All files transferred')
