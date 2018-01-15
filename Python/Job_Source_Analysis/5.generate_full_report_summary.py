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

def generate_single_job_summary(source_file_list):
    row_dict = {"job_guid":"",
                "MW_version": "",
                "well_name": "",
                "client_name": "",
                "work_flow": "",
                "simulator": "",
                "machine_name": ""}
    for f in source_file_list:
        print(f)
        file = open(f, encoding="utf8")
        content = file.read()
        job_guid = find("JobGUID=",";",content)
        MW_version = find("MWVersion=",r'\n',content)
        well_name = find("WellName=", r';', content)
        client_name = find("ClientName=", r';', content)
        work_flow = find("Workflow=", r';', content)
        simulator = find("Simulator=", r';', content)
        machine_name = find("MachineName=", r';', content)
        file.close()
        row_dict["job_guid"] = row_dict["job_guid"] if job_guid == "" else job_guid
        row_dict["MW_version"] = row_dict["MW_version"] if MW_version == "" else MW_version
        row_dict["well_name"] = row_dict["well_name"] if well_name == "" else well_name
        row_dict["client_name"] = row_dict["client_name"] if client_name == "" else client_name
        row_dict["work_flow"] = row_dict["work_flow"] if work_flow == "" else work_flow
        row_dict["simulator"] = row_dict["simulator"] if simulator == "" else simulator
        row_dict["machine_name"] = row_dict["machine_name"] if machine_name == "" else machine_name

    return row_dict

def find(start, end, inputtext):
    result = []
    search = r'(?<={}).*?(?={})'.format(start, end)
    for matchedtext in re.findall(search, inputtext):
        result.append(matchedtext)

    if(len(result) > 0):
        return result[0]
    else:
        return ""

def generate_summary_csv(summary):
    with open(r'd:\names.csv', 'w', newline='',encoding="utf-8") as csvfile:
        fieldnames = ["job_guid",
                    "MW_version",
                    "well_name",
                    "client_name",
                    "work_flow",
                    "simulator",
                    "machine_name"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary:
            writer.writerow(row[0])
    return



def copy_given_version_files(summary, mw_versions):
    for row in summary:
        if row[0]['MW_version'] in mw_versions and row[0]['simulator'] == 'False':
            for path in row[1]:
                shutil.copy2(path, r'd:\3')
    return

source_dir = "D:\\2\\"
#source_dir = r'D:\analytics\2'
maps = build_job_file_map(source_dir);

summary = []
for job_guid in maps:
    row_dict = generate_single_job_summary(maps[job_guid])
    summary.append((row_dict, maps[job_guid]))

generate_summary_csv(summary)
copy_given_version_files(summary, ['8.0.95333.3100','8.0.94233.3100','8.0.92053.3100'])

print(str(__file__) + "done")