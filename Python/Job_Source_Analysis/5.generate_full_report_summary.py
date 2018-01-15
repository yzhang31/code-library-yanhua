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
                "job_name":"",
                "MW_version": "",
                "well_name": "",
                "client_name": "",
                "work_flow": "",
                "simulator": "",
                "machine_name": "",
                "RTBackupDir": None,
                "SON":None,
                "LUN": None,
                "LUL":None,
                "LATI":None,
                "LONG":None}
    for f in source_file_list:
        print(f)
        file = open(f, encoding="utf8")
        content = file.read()
        job_guid = find("JobGUID=",";",content)
        job_name = find("JobName=",";",content)
        MW_version = find("MWVersion=",r'\n',content)
        well_name = find("WellName=", r';', content)
        client_name = find("ClientName=", r';', content)
        work_flow = find("Workflow=", r';', content)
        simulator = find("Simulator=", r';', content)
        machine_name = find("MachineName=", r';', content)
        RTBackupDir = find("RTBackupDir=", r';', content)
        SON = find("OSDD=SON", r'', content)
        LUN = find("OSDD=LUN", r'', content)
        LUL = find("OSDD=LUL", r'', content)
        LATI = find("Enter Longitude,Input,TextBox,", r',UIInteraction', content)
        LONG = find("Enter Latitude,Input,TextBox", r',UIInteraction', content)

        file.close()
        row_dict["job_guid"] = row_dict["job_guid"] if job_guid == None else job_guid
        row_dict["job_name"] = row_dict["job_name"] if job_guid == None else job_name
        row_dict["MW_version"] = row_dict["MW_version"] if MW_version == None else MW_version
        row_dict["well_name"] = row_dict["well_name"] if well_name == None else well_name
        row_dict["client_name"] = row_dict["client_name"] if client_name == None else client_name
        row_dict["work_flow"] = row_dict["work_flow"] if work_flow == None else work_flow
        row_dict["simulator"] = row_dict["simulator"] if simulator == None else simulator
        row_dict["machine_name"] = row_dict["machine_name"] if machine_name == None else machine_name
        row_dict["RTBackupDir"] = row_dict["RTBackupDir"] if RTBackupDir == None else RTBackupDir
        row_dict["SON"] = row_dict["SON"] if SON == None else SON
        row_dict["LUN"] = row_dict["LUN"] if LUN == None else LUN
        row_dict["LUL"] = row_dict["LUL"] if LUL == None else LUL
        row_dict["LATI"] = row_dict["LATI"] if LATI == None else LATI
        row_dict["LONG"] = row_dict["LONG"] if LONG == None else LONG

    return row_dict


def generate_single_job_summary(source_file_list):
    row_dict = {"job_guid":"",
                "job_name":"",
                "MW_version": "",
                "well_name": "",
                "client_name": "",
                "work_flow": "",
                "simulator": "",
                "machine_name": "",
                "RTBackupDir": None,
                "SON":None,
                "LUN": None,
                "LUL":None,
                "LATI":None,
                "LONG":None,
                "BLI":None}
    for f in source_file_list:
        print(f)
        file = open(f, encoding="utf8")
        content = file.read()
        job_guid = find("JobGUID=",";",content)
        job_name = find("JobName=",";",content)
        MW_version = find("MWVersion=",r'\n',content)
        well_name = find("WellName=", r';', content)
        client_name = find("ClientName=", r';', content)
        work_flow = find("Workflow=", r';', content)
        simulator = find("Simulator=", r';', content)
        machine_name = find("MachineName=", r';', content)
        RTBackupDir = find("RTBackupDir=", r';', content)
        SON = find("OSDD=SON", r'', content)
        LUN = find("OSDD=LUN", r'', content)
        LUL = find("OSDD=LUL", r'', content)
        LATI = find("Enter Longitude,Input,TextBox,", r',UIInteraction', content)
        LONG = find("Enter Latitude,Input,TextBox", r',UIInteraction', content)
        BLI = find("Enter BLI,Input,TextBox,", r',UIInteraction', content)

        file.close()
        row_dict["job_guid"] = row_dict["job_guid"] if job_guid == None else job_guid
        row_dict["job_name"] = row_dict["job_name"] if job_guid == None else job_name
        row_dict["MW_version"] = row_dict["MW_version"] if MW_version == None else MW_version
        row_dict["well_name"] = row_dict["well_name"] if well_name == None else well_name
        row_dict["client_name"] = row_dict["client_name"] if client_name == None else client_name
        row_dict["work_flow"] = row_dict["work_flow"] if work_flow == None else work_flow
        row_dict["simulator"] = row_dict["simulator"] if simulator == None else simulator
        row_dict["machine_name"] = row_dict["machine_name"] if machine_name == None else machine_name
        row_dict["RTBackupDir"] = row_dict["RTBackupDir"] if RTBackupDir == None else RTBackupDir
        row_dict["SON"] = row_dict["SON"] if SON == None else SON
        row_dict["LUN"] = row_dict["LUN"] if LUN == None else LUN
        row_dict["LUL"] = row_dict["LUL"] if LUL == None else LUL
        row_dict["LATI"] = row_dict["LATI"] if LATI == None else LATI
        row_dict["LONG"] = row_dict["LONG"] if LONG == None else LONG
        row_dict["BLI"] = row_dict["BLI"] if BLI == None else BLI

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
        fieldnames = ["job_guid",
                      "job_name",
                    "MW_version",
                    "well_name",
                    "client_name",
                    "work_flow",
                    "simulator",
                    "machine_name",
                      "RTBackupDir",
                      "SON",
                      "LUN",
                      "LUL",
                      "LATI",
                      "LONG",
                      "BLI"]

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

print(str(__file__) + "done")