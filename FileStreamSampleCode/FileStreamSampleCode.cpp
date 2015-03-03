// FileStreamSampleCode.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <sstream>

using namespace std;


int _tmain(int argc, _TCHAR* argv[])
{
    std::string input = "41 3.14 false hello world";
    std::istringstream stream(input);
    int n;
    double f;
    bool b;

    stream >> n >> f >> std::boolalpha >> b;
    std::cout << "n = " << n << '\n'
        << "f = " << f << '\n'
        << "b = " << std::boolalpha << b << '\n';

    // extract the rest using the streambuf overload
    stream >> std::cout.rdbuf();

    double tmp = -1.0;

    std::cout << stream.eof() << endl;

    for (size_t i = 0; i < 10; i++)
    {
        stream >> tmp;
        std::cout << tmp << '\n';
    }
        
    stream >> tmp;
    std::cout << tmp << '\n';
}

