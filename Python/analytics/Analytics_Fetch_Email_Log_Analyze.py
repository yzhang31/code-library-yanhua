import os
import re
import shutil

def CopySMLZipFileWithFilter(source_dir):
    for root, dirs, files in os.walk(os.path.abspath(source_dir)):
        for file in files:
            if ("FetchFilesSendByEmailTHM" not in str(file)) :
                continue
            full_path = os.path.join(root, file)
            pos = str(file).find(".")
            timestring = str(file)[pos+1:pos+9]
            if int(timestring) < 20180322:
                continue
            f = open(full_path,  encoding="utf8")
            content = f.read()
            results = find("TotalItemCount: ", r'\n', content)
            print(timestring, ",",sum([int(i) for i in results]))
    return

def find(start, end, inputtext):
    result = []
    search = r'(?<={}).*?(?={})'.format(start, end)
    for matchedtext in re.findall(search, inputtext):
        result.append(matchedtext)

    return result

source_path = r'\\analytics\working\logbackup'
#source_path = r'D:\temp'

CopySMLZipFileWithFilter(source_path)
