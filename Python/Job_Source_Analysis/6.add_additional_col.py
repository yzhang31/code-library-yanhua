import csv


def process(input_file, ref_csv_file, output_file):
    #read ref file into dict {jobuid:type}
    csv.field_size_limit(100000000)
    ref_guid_jobtype_dict = {}
    with open(ref_csv_file, 'r', encoding="utf-8") as ref_csv:
        dict_reader = csv.DictReader(ref_csv,quoting = csv.QUOTE_NONE)
        for row in dict_reader:
            ref_guid_jobtype_dict[str(row["JOB_GUID"]).upper()] = row["JOB_SOURCE"]
    #write additional column into output csv.
    with open(input_file, 'r',encoding="utf-8") as csvinput:
        with open(output_file, 'w', newline='',encoding="utf-8") as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            row.append('Ref Source')
            all.append(row)

            for row in reader:
                if (row[0].upper() in ref_guid_jobtype_dict):
                    row.append(ref_guid_jobtype_dict[row[0].upper()])
                else:
                    row.append("Not found")

                all.append(row)

            writer.writerows(all)

input_file = r'd:\job_info_summary.csv'
output_file = r'd:\job_info_summary_with_ref.csv'
ref_csv_path = r'd:\work\2018_01_11_Job_Source_Study\2018_01_17_analytics_jobsummary.csv'

process(input_file, ref_csv_path, output_file)

print(str(__file__) + " : done")