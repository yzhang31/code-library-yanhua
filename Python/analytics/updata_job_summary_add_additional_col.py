import csv


def process(input_file, ref_csv_file, output_file):
    #read ref file into dict {jobuid:type}
    csv.field_size_limit(100000000)
    ref_guid_jobtype_dict = {}
    with open(ref_csv_file, 'r', encoding="utf-8") as ref_csv:
        for line in ref_csv.readlines():
            line = line.replace(', \n', "")
            seps = line.split(",",1)
            ref_guid_jobtype_dict[seps[0].upper()] = seps[1]

    #write additional column into output csv.
    with open(input_file, 'r',encoding="utf-8") as csvinput:
        with open(output_file, 'w', newline='',encoding="utf-8") as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)
            all = []
            row = next(reader)
            row.append('Ref Operations')
            all.append(row)

            for row in reader:
                if (row[0].upper() in ref_guid_jobtype_dict):
                    row.append(ref_guid_jobtype_dict[row[0].upper()])
                else:
                    row.append("Not found")

                all.append(row)

            writer.writerows(all)

input_file = r'd:\jobsummary.csv'
output_file = r'd:\MTBF_JobSummary_With_Operations.csv'
ref_path = r'd:\Temp\newJoblog.txt'

process(input_file, ref_path, output_file)

print(str(__file__) + " : done")