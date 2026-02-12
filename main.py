import os
import shutil


update_existing = True

# to
redirect_path = 'C:\your\new\path\DJI_001'

# from
target_path = 'F:\DCIM\DJI_001'

notice_when_file_copied = True
notice_when_file_already_existed = True
notice_when_folder_already_existed = True
notice_when_folder_created = True

def check_existing_folders():
    global existing_folders
    
    check_path = os.walk(redirect_path)

    existing_folders = {}
    for root, dirs, files in check_path:
        
        path = str(root)
        if path == redirect_path:
            continue
        # root : C:\photos\folder\subfolder
        # redirect_path : C:\photos\new_folder\name
        path = path[len(redirect_path)+1:len(redirect_path)+11]
        root = root[len(redirect_path)+1:]
        # path : subfolder
        # root : subfolder or subfolder...

        existing_folders.update({path : root})


check_existing_folders()


def create_dir(name):
    global redirect_path
    
    if name in existing_folders:
        if notice_when_folder_already_existed: 
            print(f'Folder {name} already exists')
        return
    try:
        os.mkdir(f'{redirect_path}\{name}')
    except FileExistsError:

        if notice_when_folder_already_existed: 
            print(f'Folder {name} already exists')

    else:
        if notice_when_folder_created:
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
            
            # extract date from file name

            date = file.split('_')
            date = date[1]
            date = date[:8]
            # date : yyyymmdd

            # check if folder already exists
            new_folder_name = f'{date[:4]}_{date[4:6]}_{date[6:10]}'
            if date not in date_set:
                date_set.add(date)
                # new_folder_name : yyyy_mm_dd
                create_dir(new_folder_name)
            
            # rename the new folder if it already exists
            if new_folder_name in existing_folders.keys():
                new_folder_name = existing_folders[new_folder_name]


            # check if file already exists in new location
            if os.path.exists(f'{redirect_path}\\{new_folder_name}\\{file}'):
                if notice_when_file_already_existed:
                    print(f'File {file} already exists in folder {new_folder_name}')                # testing
                continue
            elif notice_when_file_copied:
                print(f'Copying file {file} to folder {new_folder_name}')


            shutil.copyfile(f'{target_path}\\{file}',f'{redirect_path}\\{new_folder_name}\\{file}')

        else:
            raise Exception('File unexpected', file)
        
if 'root' not in locals():
    raise Exception('No files found in target path')
print('All files transferred')
