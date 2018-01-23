import os
from os import listdir
from os.path import isfile, join
import shutil
import zipfile




def CopySMLZipFileWithFilter(source_dir, dst_dir : str, filter_time):
	if not (os.path.exists(dst_dir)):
		os.makedirs(dst_dir)
	for root, dirs, files in os.walk(os.path.abspath(source_dir)):
		for file in files:
			if ("zip" not in str(file)) \
					or ("FieldImage" not in str(file)) \
					or ("WinchsafeSystemMonitor" in str(file)) \
					or ("@HPV" in str(file)) \
					or ("@BGC-QA" in str(file)) \
					or ("@MW-QA" in str(file)):
				continue
			pos = str(file).rfind("@")
			timestring = str(file)[pos+1:pos+15]
			print(timestring)
			need_copy = False
			if(int(timestring) > filter_time):
				full_path = os.path.join(root, file)
				try:
					with zipfile.ZipFile(full_path,'r') as zFile:
						for name in zFile.namelist():
							if(name.endswith(".dmp") and 'ExeJobManager.' in str(name)):
								need_copy = True
								break
				except:
					continue
			if(need_copy):
				print(file)
				shutil.copy2(full_path,dst_dir)
	print("CopySMLZipFileWithFilter Finished.")

filter_time = 20170601000000
target_dir = r'D:\dump.1'
mypath = "\\\\srv004bgc.dir.slb.com\\MaxwellAnalytics\\ArchiveBackup\\"
#mypath = r'D:\dump.0'
CopySMLZipFileWithFilter(mypath, target_dir, filter_time)
