import os
from os import listdir
from os.path import isfile, join
import shutil

def CopySMLZipFileWithFilter(source_dir, dst_dir, filter_time):
    scaned_total_file_count = 0
    for root, dirs, files in os.walk(os.path.abspath(source_dir)):
        scaned_total_file_count += len(files)
        for file in files:
            if ("zip" not in str(file)) or ("FieldImage" not in str(file)) or ("WinchsafeSystemMonitor" in str(file)):
                continue
            pos = str(file).rfind("@")
            timestring = str(file)[pos+1:pos+15]
            if(int(timestring) > filter_time):
                full_path = os.path.join(root, file)
                try:
                    print("copy file ..." + str(file))
                    shutil.copy2(full_path, dst_dir)
                except:
                    continue
    print("CopySMLZipFileWithFilter Finished." + "Scanned File {0}".format(scaned_total_file_count))

filter_time = 20170726000000
target_dir = "D:\\1\\"
#source_path = "D:\\2\\"
source_path = "\\\\srv004bgc.dir.slb.com\\MaxwellAnalytics\\ArchiveBackup\\"
CopySMLZipFileWithFilter(source_path, target_dir, filter_time)
