import os
from os import listdir
from os.path import isfile, join
import shutil
import zipfile
import re
import csv

def build_job_guid(file_name):
    seps = str(file_name).split("_")
    return seps[-5]

def build_valid_job_guid_info(csv_path):
    job_infos = {}
    with open(csv_path, 'r', newline='', encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for jobinfo in reader:
            row = {'job_guid': jobinfo['job_guid'],'MW_version':jobinfo['MW_version'], 'work_flow':jobinfo['work_flow'], 'simulator':jobinfo['simulator']}
            need_copy = check_job_guid_info(row)
            if(need_copy):
                job_infos[str(jobinfo['job_guid']).upper()] = row
    return job_infos

def check_job_guid_info(job_info):
    if(job_info['simulator'] == 'True'):
        return False

    taget_versions = ['95333','92053','94233']
    if any(version in job_info['MW_version'] for version in taget_versions):
        return  True

    return False

def group_files_via_workflows(source_path, dest_path, summary):

    for root, dirs, files in os.walk(os.path.abspath(source_dir)):
        for file in files:
            full_path = os.path.join(root, file)
            guid = build_job_guid(file)
            if(guid.upper() in summary):
                print('copy ... {0}'.format(str(file)))
                shutil.copy2(full_path, dest_path)

source_dir = r'\\srv004bgc.dir.slb.com\MaxwellShareData\Core\Computation\YZhang31\analytics\user_operations\2'

csv_path = r'd:\4\job_summary_no_empty_line.csv'

info_dict = build_valid_job_guid_info(csv_path)

group_files_via_workflows(source_dir, r'd:\5', info_dict)
#loop files in source dir.

print(str(__file__) + "done")