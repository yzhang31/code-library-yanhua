import os
from os import listdir
from os.path import isfile, join
import shutil
import csv
import re


def find(start, end, inputtext):
    result = set()
    search = r'(?<={}).*?(?={})'.format(start, end)
    for matchedtext in re.findall(search, inputtext):
        result.add(matchedtext)

    if(len(result) > 0):
        return '/'.join(result)
    else:
        return None

def dump_analyze(source_dir, dst_dir):
	if not (os.path.exists(dst_dir)):
		os.makedirs(dst_dir)

	for root, dirs, files in os.walk(os.path.abspath(source_dir)):
		for file in files:
			full_path = os.path.join(root, file)

			f = open(full_path, encoding="utf8")
			content = f.read()

			threads = content.split("Id: ")

			for	itme in threads:
				if ("CSlbError" in itme) or ("Exception" in itme):
					if ("computation" in itme):
						shutil.copy2(full_path, dst_dir)


dump_analyze( r'D:\dump.4', r'D:\dump.5')

