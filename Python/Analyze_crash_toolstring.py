import os
from os import listdir
from os.path import isfile, join
import shutil
import zipfile


def CopySMLZipFileWithFilter(source_dir):
	namelist = []
	for root, dirs, files in os.walk(os.path.abspath(source_dir)):
		for file in files:
			full_path = os.path.join(root, file)
			namelist.append(full_path)
			print(full_path)

	return namelist
pairs=[]

active_start = False
active_start_line = ""

def Reset():
    global  active_start
    global  active_start_line
    active_start = False
    active_start_line = ""

def process_line(line):
    global  active_start
    global  active_start_line

    if "Activate Run" in line:
        active_start = True
        active_start_line = line
    elif "Confirm to Stop Run" in line:
        Reset()
        print("Skip one")
    elif "CrashSeverity=critical" in line:
        if active_start == True:
            pairs.append((active_start_line, line))
            Reset()


names = CopySMLZipFileWithFilter("D:\\\\temp")

for filename in names:
    with open(filename) as f:
        Reset()
        for line in f:
            process_line(line)

for line in pairs:
    print(line)