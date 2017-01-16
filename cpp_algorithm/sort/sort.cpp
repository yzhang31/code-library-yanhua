// sort.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "vector"
#include "iostream"
#include "algorithm"

using namespace std;


void output_array(vector<int>& array)
{
	for (auto val : array)
	{
		cout << val << ",";
	}
	cout << endl;
}


void bubble_sort(vector<int>& unsorted_array)
{
	cout << "bubble_sort" << endl;

	int compare_count = 0;
	for (auto i = unsorted_array.begin(); i != unsorted_array.end(); i++)
	{
		for (auto j = unsorted_array.end() - 1; j != i; j--)
		{
			if (*(j - 1) > *j)
			{
				swap(*(j - 1), *j);
			}
			compare_count++;
		}
		output_array(unsorted_array);
	}
	cout << "Total Compare Count:" << compare_count << endl;
}

void bubble_sort2(vector<int>& unsorted_array)
{
	cout << "bubble_sort2" << endl;
	int compare_count = 0;

	for (auto i = unsorted_array.begin(); i != unsorted_array.end(); i++)
	{
		int flag = 0;
		for (auto j = unsorted_array.end() - 1; j != i; j--)
		{
			if (*(j - 1) > *j)
			{
				swap(*(j - 1), *j);
				flag = 1;
			}
			compare_count++;
		}
		output_array(unsorted_array);
		if (!flag)
		{
			break;
		}
	}
	cout << "Total Compare Count:" << compare_count << endl;
}


void bubble_sort_wrong(vector<int>& unsorted_array)
{
	cout << "bubble_sort_wrong" << endl;

	int compare_count = 0;
	for (auto i = unsorted_array.begin(); i != unsorted_array.end(); i++)
	{
		for (auto j = i + 1; j != unsorted_array.end(); j++)
		{
			if (*j < *i)
			{
				swap(*j, *i);
			}
			compare_count++;
		}
		output_array(unsorted_array);
	}
	cout << "Total Compare Count:" << compare_count << endl;
}

void bubble_sort2_wrong(vector<int>& unsorted_array)
{
	cout << "bubble_sort2_wrong" << endl;
	int compare_count = 0;
	for (auto i = unsorted_array.begin(); i != unsorted_array.end(); i++)
	{
		int flag = 0;
		for (auto j = i + 1; j != unsorted_array.end(); j++)
		{
			if (*j < *i)  // should compare j and j-1;
			{
				swap(*j, *i);
				flag = 1;
			}
			compare_count++;
		}
		output_array(unsorted_array);
		if (!flag)
		{
			break;
		}

	}
	cout << "Total Compare Count:" << compare_count << endl;

}



int main()
{
	//vector<int> unsorted_array = {2,1,3,4,5,6,0,7,8};

	vector<int> unsorted_array = { 0, 7,8,5,2,1,3,4,6 }; // wrong bubble_sort2_wrong cannot handle.

	cout << "original" << endl;
	output_array(unsorted_array);
	cout << endl;


	vector<int> v1(unsorted_array);
	vector<int> v2(unsorted_array);


	bubble_sort(vector<int>(unsorted_array));
	bubble_sort2(vector<int>(unsorted_array));
	bubble_sort_wrong(vector<int>(unsorted_array));
	bubble_sort2_wrong(vector<int>(unsorted_array));

    return 0;
}

