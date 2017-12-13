import os
from os import listdir
from os.path import isfile, join
import shutil
import zipfile


def ListFullPathFileWithFilter(source_dir, dump_sub_str):
	file_list = []
	for root, dirs, files in os.walk(os.path.abspath(source_dir)):
		for file in files:
			if (dump_sub_str not in str(file)):
				continue
			full_path = os.path.join(root, file)
			file_list.append(full_path)
	return file_list

files = ListFullPathFileWithFilter("d:\\exejob2\\",".dmp")
print(files)

cdb = "d:\\Apps\\dev\\windbg\\cdb.exe  -c \"~*k;q\"  -z "

for x in files:
	cmd = cdb + x +" > " + x + ".log"
	log_file = x + ".log"
	os.system(cmd);
	if "MaxWell :: 8." in open(log_file).read():
		shutil.copy2(x,"d:\\exejob2_result\\")		
		shutil.copy2(log_file,"d:\\exejob2_result\\")