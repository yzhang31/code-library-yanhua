import os
from os import listdir
from os.path import isfile, join
import shutil
import csv
import re


def get_job_guid(filename):
    file = open(filename, encoding="utf8")
    content = file.read()
    re_result = find ("JobGuid :: ","\|JobName", content)
    file.close()
    return re_result




def find(start, end, inputtext):
    result = set()
    search = r'(?<={}).*?(?={})'.format(start, end)
    for matchedtext in re.findall(search, inputtext):
        result.add(matchedtext)

    if(len(result) > 0):
        return '/'.join(result)
    else:
        return None

def dump_analyze(source_dir, dst_dir,ref_csv_file):
	if not (os.path.exists(dst_dir)):
		os.makedirs(dst_dir)

	csv.field_size_limit(100000000)
	ref_guid_jobtype_dict = {}
	with open(ref_csv_file, 'r', encoding="utf-8") as ref_csv:
		dict_reader = csv.DictReader(ref_csv, quoting=csv.QUOTE_NONE)
		for row in dict_reader:
			ref_guid_jobtype_dict[str(row["JOB_GUID"]).upper()] = row["JOB_TYPE"]
	# write additional column into output csv.

	for root, dirs, files in os.walk(os.path.abspath(source_dir)):
		for file in files:
			full_path = os.path.join(root, file)

			jobguid = get_job_guid(full_path)
			if jobguid == None: continue
			if(jobguid.upper() in ref_guid_jobtype_dict):
				work_flow = ref_guid_jobtype_dict[jobguid.upper()]
				if work_flow == "D&M":
					shutil.copy2(full_path, dst_dir)


ref_csv_path = r'd:\work\2018_01_11_Job_Source_Study\2018_01_17_analytics_jobsummary.csv'
dump_analyze(r'D:\dump.3', r'D:\dump.4',ref_csv_path)

