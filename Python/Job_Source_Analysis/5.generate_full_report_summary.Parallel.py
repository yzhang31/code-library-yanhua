import os
from collections import OrderedDict
import re
import csv
import os, multiprocessing as mp
import time

def build_job_file_map(source_dir):
    guid_files_map = {}
    for root, dirs, files in os.walk(os.path.abspath(source_dir)):
        for file in files:
            full_path = os.path.join(root, file)
            guid = extrac_guid_from_filename(file)
            machine_name = extrac_machine_name_from_filename(full_path)
            #filter out VM.
            if  (machine_name.startswith("BGC-QA") or machine_name.startswith("HPV")
                    or machine_name.startswith("MW-QA"))\
                    or "HYPERV" in machine_name:
                continue

            if(guid in guid_files_map):
                guid_files_map[guid].append(str(full_path))
            else:
                guid_files_map[guid] = [str(full_path)]
    return  guid_files_map

def extrac_guid_from_filename(file_name):
    seps = str(file_name).split("_")
    return seps[-5]

def extrac_machine_name_from_filename(file_name):
    seps = str(file_name).split("@")
    seps = seps[1].split("__")
    return seps[0]


extact_infos = [("job_guid","","JobGUID=",";"),
                ("job_name","","JobName=",";"),
                ("MW_version","","MWVersion=",r'\n'),
                ("well_name","","WellName=",";"),
                ("client_name","","ClientName=",";"),
                ("start_date","",";StartDate=",";Workflow="),
                ("work_flow","","Workflow=",";"),
                ("simulator","","Simulator=",";"),
                ("machine_name","","MachineName=",";"),
                ("Engineer Name", None,"Enter engineer name,Input,TextBox,",",UIInteraction,RunGuid"),
                ("RTBackupDir","","RTBackupDir=",";"),
                ("SON", None, "GridCell,", r',UIInteraction,OSDD=SON'),
                ("LUN", None, "GridCell,", r',UIInteraction,OSDD=SON'),
                ("CONT_REGION", None, "GridCell,", r',UIInteraction,OSDD=CONT_REGION'),
                ("LATI", None, "Enter Latitude,Input,TextBox", r',UIInteraction'),
                ("LONG", None, "Enter Longitude,Input,TextBox,", r',UIInteraction'),
                ("BLI", None, "Enter BLI,Input,TextBox,", r',UIInteraction'),
                ("WL Station/Pass Started", None, "WLAcquisition,Data Acquiring - WL,Start ", r' Pass,Click,Button,Start,UIInteraction,'),
                ("Generate Dliverables", None, "Create/Publish...,UIInteraction,ComponentName=", r';DelivTemplateGuid'),
                ("Open Shop Calibration", None, "Setup,Equipment,", r' ToolString for Shop Calibration,Click,ContextMenu,Activate for Checks and Calibration,'),
                ("Connect HSPM", None, r'DnMAcquisition,Data Acquiring - D&M,HSPM Control/', r',Click,Button,Connect,UIInteraction'),
                ("Connect InterACT", None, r'ComponentName=WITSML Standard;ComponentCode=Component_Template_Witsml;Publisher=', r'\n'),
                ("Create JA/RA", None, r'ArchiveGuid=', r'\n'),
                ("Create PDF", None, r'Graphical,Print/Create PDF for Template,Click,ContextMenu,Print/PDF', r'\n'),
                ("IPAddress_1", None, r'IPAddress_1=', r';'),
                ("IPAddress_2", None, r'IPAddress_2=', r';')
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

    op_counts = analyze_job_operations(source_file_list)

    row_dict.update(op_counts)

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


def callback(item):
    global processed_file_numbers
    processed_file_numbers += 1
    print(r'{0:.2f}% progress... The {1} file in {2} files.'
          .format((processed_file_numbers / total_file_numbers) * 100,
          processed_file_numbers,
          total_file_numbers))

def process_data_parallel(guid_files_map):
    summary = []
    results = []
    pool = mp.Pool()
    for job_guid in guid_files_map:
        proc = pool.apply_async(generate_single_job_summary, args=[guid_files_map[job_guid]], callback = callback)
        results.append(proc)
    pool.close()
    pool.join()
    # iterate through results
    for proc in results:
        processfile_result = proc.get()
        summary.append((processfile_result))

    return summary


def process_data_parallel_map(guid_files_map):
    progress = 0
    summary = []
    results = []
    pool = mp.Pool()

    results = pool.map(generate_single_job_summary,guid_files_map.values())

    pool.close()
    pool.join()
    # iterate through results
    for proc in results:
        processfile_result = proc.get()
        summary.append((processfile_result))

    return summary

if __name__ == "__main__":
    start = time.clock()
    processed_file_numbers = 0
    total_file_numbers = 0

    source_dir = "D:\\5\\"
    guid_files_map = build_job_file_map(source_dir)
    total_file_numbers =  len(guid_files_map)
    summary = process_data_parallel(guid_files_map)
    #summary = process_data_parallel_map(guid_files_map)
    generate_summary_csv(summary)

    elapsed = (time.clock() - start)

    print(str(__file__) + " : done {0} s".format(elapsed))