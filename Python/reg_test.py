import os
import re


def test(text):

    for matchedtext in re.findall(r'(?<=JobGUID=).*?(?=;)', text):
        print(matchedtext)

    for matchedtext in re.findall(r'(?<=MWVersion=).*?(?=\n)', text):
        print(matchedtext)

    for matchedtext in re.findall(r'(?<=MWVersion=).*?(?=$)', text):
        print(matchedtext)

def find(start, end, inputtext):
    result = []
    search = r'(?<={}).*?(?={})'.format(start, end)
    for matchedtext in re.findall(search, inputtext):
        result.append(matchedtext)

    if(len(result) > 0):
        return result[0]
    else:
        return None
content = "JobName=17OKC0656;WellName=GRANT 2-2-35WH;ClientName=CALYX ENERGY;StartDate=12/31/2017 11:00 AM;Workflow=D&M;Simulator=False;UnitSystem=English;JobSize=0;State=Available;SideTrackId=0;SessionID=ABBA68C5-8847-4549-8C60-F3095CB4CDE8;SortOrder=1;JobGUID=A336A3AB-AD33-4C54-BA38-48D0D7784B5F;WellGUID=A00A0936-507D-471D-B341-B82D71737BB5;;MWVersion=8.0.95333.3100\n"
content2 = "42942.9398347106,Setup,Well Setup (Internal),Change Property Value,Update,GridCell,FX004,UIInteraction,OSDD=LUN"
maps = test(content);

r1 = find("MachineName=", r';', content)

LUL = find("GridCell,", r',UIInteraction,OSDD=LUL', content2)
LUN = find("GridCell,", r',UIInteraction,OSDD=LUN', content2)

print(str(__file__) + " done")