// get_file_name_increased.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;


string GetIncreasedFileName()
{

	int i = 0;
	while (true)
	{
		std::ostringstream osstream;
		osstream.clear();
		osstream << "D:\\test_" << i;
		string filename = osstream.str();
		ifstream infile(filename);
		if (!infile.good())
		{
			return filename;
		}
		else
		{
			i++;
			continue;
		}
	}
}

int main()
{
	for (size_t i = 0; i < 10; i++)
	{
		std::string filename = getIncreasedFileName();
		ofstream newfile(filename);
	}
    return 0;
}


