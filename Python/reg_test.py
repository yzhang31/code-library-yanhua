import os
import re


def test(text):

    for matchedtext in re.findall(r'(?<=JobGUID=).*?(?=;)', text):
        print(matchedtext)

    for matchedtext in re.findall(r'(?<=MWVersion=).*?(?=\n)', text):
        print(matchedtext)

    for matchedtext in re.findall(r'(?<=MWVersion=).*?(?=$)', text):
        print(matchedtext)


maps = test("JobName=17OKC0656;WellName=GRANT 2-2-35WH;ClientName=CALYX ENERGY;StartDate=12/31/2017 11:00 AM;Workflow=D&M;Simulator=False;UnitSystem=English;JobSize=0;State=Available;SideTrackId=0;SessionID=ABBA68C5-8847-4549-8C60-F3095CB4CDE8;SortOrder=1;JobGUID=A336A3AB-AD33-4C54-BA38-48D0D7784B5F;WellGUID=A00A0936-507D-471D-B341-B82D71737BB5;;MWVersion=8.0.95333.3100\n");


print(str(__file__) + " done")