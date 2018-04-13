import csv


def process(input_file, ref_csv_file, output_file):
    #read ref file into dict {jobuid:type}
    csv.field_size_limit(100000000)
    ref_guid_jobtype_dict = {}
    additional_cols = ['NUM_OF_TERMINAL_CRASHES','DURATION(hrs)',"JOB_SOURCE"]
    with open(ref_csv_file, 'r', encoding="utf-8") as ref_csv:
        dict_reader = csv.DictReader(ref_csv,quoting = csv.QUOTE_NONE)
        for row in dict_reader:
            ref_guid_jobtype_dict[str(row["JOB_GUID"]).upper()] = \
                [row[additional_cols[0]],row[additional_cols[1]],row[additional_cols[2]]]
    #write additional column into output csv.
    with open(input_file, 'r',encoding="utf-8") as csvinput:
        with open(output_file, 'w', newline='',encoding="utf-8") as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            row += additional_cols
            all.append(row)

            for row in reader:
                if (row[0].upper() in ref_guid_jobtype_dict):
                    row = row + ref_guid_jobtype_dict[row[0].upper()]
                else:
                    row = row +['','','Not Found']
                all.append(row)

            writer.writerows(all)

input_file = r'd:\job_info_summary.csv'
output_file = r'd:\job_info_summary_with_ref.csv'
ref_csv_path = r'd:\2018_01_17_analytics_jobsummary.csv'

process(input_file, ref_csv_path, output_file)

print(str(__file__) + " : done")