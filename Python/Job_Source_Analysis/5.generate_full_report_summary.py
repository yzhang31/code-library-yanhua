import os
from os import listdir
from os.path import isfile, join
import shutil
import zipfile
import re
import csv

def build_job_file_map(source_dir):
    guid_files_map = {}
    for root, dirs, files in os.walk(os.path.abspath(source_dir)):
        for file in files:
            full_path = os.path.join(root, file)
            guid = build_job_guid(file)
            if(guid in guid_files_map):
                guid_files_map[guid].append(str(full_path))
            else:
                guid_files_map[guid] = [str(full_path)]
    return  guid_files_map

def build_job_guid(file_name):
    seps = str(file_name).split("_")
    return seps[-5]

extact_infos = [("job_guid","","JobGUID=",";"),
                ("job_name","","JobName=",";"),
                ("MW_version","","MWVersion=",r'\n'),
                ("well_name","","WellName=",";"),
                ("client_name","","ClientName=",";"),
                ("work_flow","","Workflow=",";"),
                ("simulator","","Simulator=",";"),
                ("machine_name","","MachineName=",";"),
                ("RTBackupDir","","RTBackupDir=",";"),
                ("SON", None, "GridCell,", r',UIInteraction,OSDD=SON'),
                ("LUN", None, "GridCell,", r',UIInteraction,OSDD=SON'),
                ("LATI", None, "Enter Latitude,Input,TextBox", r',UIInteraction'),
                ("LONG", None, "Enter Longitude,Input,TextBox,", r',UIInteraction'),
                ("BLI", None, "Enter BLI,Input,TextBox,", r',UIInteraction'),
                ("Active Run", None, "Setup,Equipment,", r', Run,Click,Button,Activate,UIInteraction,')]

def generate_single_job_summary(source_file_list):
    global extact_infos
    row_dict = dict((a,b) for a,b,c,d in extact_infos)
    for f in source_file_list:
        print(f)
        file = open(f, encoding="utf8")
        content = file.read()

        for item in extact_infos:
            re_result = find (item[2],item[3],content)
            if not ( re_result == None):
                row_dict[item[0]] = re_result
        file.close()
    return row_dict

def find(start, end, inputtext):
    result = []
    search = r'(?<={}).*?(?={})'.format(start, end)
    for matchedtext in re.findall(search, inputtext):
        result.append(matchedtext)

    if(len(result) > 0):
        return result[0]
    else:
        return None

def generate_summary_csv(summary):
    with open(r'd:\job_info_summary.csv', 'w', newline='',encoding="utf-8") as csvfile:
        fieldnames = [a for a,b,c,d in extact_infos]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary:
            writer.writerow(row)
    return

source_dir = "D:\\5\\"

guid_files_map = build_job_file_map(source_dir)

summary = []
for job_guid in guid_files_map:
    row_dict = generate_single_job_summary(guid_files_map[job_guid])
    summary.append((row_dict))

generate_summary_csv(summary)
print(str(__file__) + " : done")