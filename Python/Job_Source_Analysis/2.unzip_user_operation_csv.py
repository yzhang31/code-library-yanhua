import os
from os import listdir
from os.path import isfile, join
import shutil
import zipfile

def unzip_user_operation_files(source_dir, dst_dir):
     for root, dirs, files in os.walk(os.path.abspath(source_dir)):
        for file in files:
            need_process = False
            full_path = os.path.join(root, file)
            try:
                with zipfile.ZipFile(full_path,'r') as zFile:
                    for name in zFile.namelist():
                        if("UserOperation" in name):
                            need_process = True
                            break
                    if(need_process):
                        print("unzip... " + str(file))
                        zFile.extractall(dst_dir)
            except:
                print("exception... " + str(file))
                continue


def delete_file_with_filter(source_dir, filter):
    for root, dirs, files in os.walk(os.path.abspath(source_dir)):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                if (filter in str(file)):
                    print("delete... " + str(file))
                    os.remove(full_path)
            except:
                print("exception... " + str(file))
                continue

source_path = "D:\\1\\"
target_dir = "D:\\2\\"
unzip_user_operation_files(source_path, target_dir)
delete_file_with_filter(target_dir, "Independent")
print(str(__file__) + "done")