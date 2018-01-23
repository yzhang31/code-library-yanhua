import os
from collections import OrderedDict
import re
import csv

def build_job_file_map(source_dir):
    guid_files_map = {}
    for root, dirs, files in os.walk(os.path.abspath(source_dir)):
        for file in files:
            full_path = os.path.join(root, file)
            guid = extrac_guid_from_filename(file)
            if(guid in guid_files_map):
                guid_files_map[guid].append(str(full_path))
            else:
                guid_files_map[guid] = [str(full_path)]
    return  guid_files_map

def extrac_guid_from_filename(file_name):
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
                ("Engineer Name", None,"Enter engineer name,Input,TextBox,",",UIInteraction,RunGuid"),
                ("RTBackupDir","","RTBackupDir=",";"),
                ("SON", None, "GridCell,", r',UIInteraction,OSDD=SON'),
                ("LUN", None, "GridCell,", r',UIInteraction,OSDD=SON'),
                ("LATI", None, "Enter Latitude,Input,TextBox", r',UIInteraction'),
                ("LONG", None, "Enter Longitude,Input,TextBox,", r',UIInteraction'),
                ("BLI", None, "Enter BLI,Input,TextBox,", r',UIInteraction'),
                ("Active Run", None, "Setup,Equipment,", r' Run,Click,Button,Activate,UIInteraction,'),
                ("WL Station/Pass Started", None, "WLAcquisition,Data Acquiring - WL,Start ", r' Pass,Click,Button,Start,UIInteraction,'),
                ("Generate Dliverables", None, "Create/Publish...,UIInteraction,ComponentName=", r';DelivTemplateGuid'),
                ("Open Shop Calibration", None, "Setup,Equipment,", r' ToolString for Shop Calibration,Click,ContextMenu,Activate for Checks and Calibration,')
                ]
def generate_single_job_summary(source_file_list):
    global extact_infos
    row_dict = dict((a,b) for a,b,c,d in extact_infos)
    for f in source_file_list:
        file = open(f, encoding="utf8")
        content = file.read()

        for item in extact_infos:
            re_result = find (item[2],item[3],content)
            if not ( re_result == None):
                row_dict[item[0]] = re_result
        file.close()
    return row_dict


def analyze_job_operations(source_file_list):

    operation_time_dict = OrderedDict()
    for f in source_file_list:
        file = open(f, encoding="utf8")
        csvReader = csv.reader(file)
        for row in csvReader:

            if(len(row) == 0): continue

            if (str(row[0]).replace('.','').isdigit()):
                operation_time_dict[row[0]] = row[1:]
        file.close()

    op_count = len(operation_time_dict.keys())
    return {"User Actions":op_count}

def find(start, end, inputtext):
    result = set()
    search = r'(?<={}).*?(?={})'.format(start, end)
    for matchedtext in re.findall(search, inputtext):
        result.add(matchedtext)

    if(len(result) > 0):
        return '/'.join(result)
    else:
        return None

def generate_summary_csv(summary):
    fieldnames = summary[0].keys()
    with open(r'd:\job_info_summary.csv', 'w', newline='',encoding="utf-8") as csvfile:
        #fieldnames = [a for a,b,c,d in extact_infos]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary:
            writer.writerow(row)
    return

def process_data(guid_files_map):
    summary = []
    progress = 0

    for job_guid in guid_files_map:
        row_dict = generate_single_job_summary(guid_files_map[job_guid])
        addition_dict = analyze_job_operations(guid_files_map[job_guid])
        row_dict.update(addition_dict)
        summary.append((row_dict))
        progress = progress + 1
        print(r'{0:.2f}% progress... The {1} file in {2} files.'.format((progress/len(guid_files_map)) * 100, progress, len(guid_files_map)))
    return summary

source_dir = "D:\\5\\"

guid_files_map = build_job_file_map(source_dir)
summary = process_data(guid_files_map)
generate_summary_csv(summary)
print(str(__file__) + " : done")