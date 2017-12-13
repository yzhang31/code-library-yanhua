import os
from os import listdir
from os.path import isfile, join
import shutil
import zipfile




def CopySMLZipFileWithFilter(source_dir, dst_dir, filter_time):
	for root, dirs, files in os.walk(os.path.abspath(source_dir)):
		for file in files:
			if ("zip" not in str(file)) or ("FieldImage" not in str(file)) or ("WinchsafeSystemMonitor" in str(file)) or ("@HPV" in str(file)) or ("@BGC-QA" in str(file)) or ("@MW-QA" in str(file)):
				continue
			pos = str(file).rfind("@")
			timestring = str(file)[pos+1:pos+15]
			print(timestring)
			need_copy = False
			if(int(timestring) > filter_time):
				full_path = os.path.join(root, file)
				with zipfile.ZipFile(full_path,'r') as zFile:
					for name in zFile.namelist():
						if(name.endswith(".dmp")):
							need_copy = True
							break
			if(need_copy):
				print(file)
				shutil.copy2(full_path,dst_dir)
	print("CopySMLZipFileWithFilter Finished.")

#\\mypath = "d:\\Temp\\"
filter_time = 20170726000000
target_dir = "D:\\1\\"
mypath = "\\\\srv004bgc.dir.slb.com\\MaxwellAnalytics\\ArchiveBackup\\"
CopySMLZipFileWithFilter(mypath, target_dir, filter_time)
