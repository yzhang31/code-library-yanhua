import os
from os import listdir
from os.path import isfile, join
import shutil
import zipfile


def unzip_user_operation_files(source_dir, dst_dir):
	if not (os.path.exists(dst_dir)):
		os.makedirs(dst_dir)
	for root, dirs, files in os.walk(os.path.abspath(source_dir)):
		for file in files:
			full_path = os.path.join(root, file)
			try:
				with zipfile.ZipFile(full_path, 'r') as zFile:
					zFile.extractall(dst_dir)
			except:
				print("exception... " + str(file))
				continue

def dump_analyze(source_dir, dst_dir):
	if not (os.path.exists(dst_dir)):
		os.makedirs(dst_dir)
	for root, dirs, files in os.walk(os.path.abspath(source_dir)):
		for file in files:
			if ('ExeJobManager' not in str(file)):
				continue
			full_path = os.path.join(root, file)
			cdb = "d:\\Apps\\dev\\windbg\\cdb.exe  -c \"~*k;q\"  -z "

			cmd = cdb + full_path + " > " + full_path + ".log"
			log_file = full_path + ".log"
			os.system(cmd)
			if "MaxWell :: 7." in open(log_file).read():
				shutil.copy2(full_path, dst_dir)
				shutil.copy2(log_file, dst_dir)

unzip_user_operation_files(r'D:\dump.1', r'D:\dump.2')

dump_analyze(r'D:\dump.2', r'D:\dump.3')